from SimpleTetris.TetriminoDef import TetriminoType
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from SimpleTetris.GameLogicTetrimino.GameLogicTetriminoModel import Tetrimino, Point

@dataclass
class GameLogicMatrixModel:
    """固定ブロックを保持する盤面モデル。

    役割は「盤面状態の保持」と「盤面に対する純粋な判定/更新」のみ。
    入力イベントの解釈やゲーム進行の判断は Updater 側で扱う。
    """
    width: int = 10
    height: int = 20
    grid: List[List[int]] = field(default_factory=list)  # 0=��, >0=�FID

    EMPTY = 0
    I_CYAN = 1
    O_YELLOW = 2
    T_PURPLE = 3
    S_GREEN = 4
    Z_RED = 5
    J_BLUE = 6
    L_ORANGE = 7

    TETRIMINO_COLORS = {
        TetriminoType.I: I_CYAN,
        TetriminoType.O: O_YELLOW,
        TetriminoType.T: T_PURPLE,
        TetriminoType.S: S_GREEN,
        TetriminoType.Z: Z_RED,
        TetriminoType.J: J_BLUE,
        TetriminoType.L: L_ORANGE,
    }

    def __init__(self, width: int = 10, height: int = 20):
        # 役割: 盤面サイズを受け取り、空セルのみの初期盤面を構築する。
        #       盤面は grid[y][x] 形式で保持する。
        self.width = width
        self.height = height
        self.grid = [[self.EMPTY for _ in range(self.width)] for _ in range(self.height)]

    def in_bounds(self, x: int, y: int) -> bool:
        """役割: 単一点座標の境界チェックを行う。"""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_empty(self, x: int, y: int) -> bool:
        """役割: 指定セルが配置可能な空状態かを返す（盤面外は False）。"""
        return self.in_bounds(x, y) and self.grid[y][x] == self.EMPTY

    def color_id_for_kind(self, kind: str) -> int:
        """役割: テトリミノ種別文字列を盤面に保存する色IDへ変換する。"""
        try:
            return self.TETRIMINO_COLORS[TetriminoType[kind]]
        except KeyError:
            # 未知の kind は空扱い色にフォールバックする
            return self.EMPTY

    def can_place(self, piece: Tetrimino, pos: Point) -> bool:
        """役割: ミノ全ブロックについて衝突/境界を検査し、配置可否を判定する。"""
        base_x, base_y = pos
        for dx, dy in piece.blocks():
            x = base_x + dx
            y = base_y + dy
            if not self.in_bounds(x, y):
                return False
            if not self.is_empty(x, y):
                return False
        return True

    def lock(self, piece: Tetrimino, pos: Point, color_id: int) -> None:
        """役割: 配置済みミノを盤面セルへ反映し、固定ブロック化する。"""
        base_x, base_y = pos
        for dx, dy in piece.blocks():
            x = base_x + dx
            y = base_y + dy
            if self.in_bounds(x, y):
                self.grid[y][x] = color_id

    def clear_lines(self) -> int:
        """役割: 満杯行を除去して上部に空行を補充し、削除行数を返す。"""
        # 全セルが埋まった行だけを取り除き、欠けた分を先頭へ補充する。
        remaining_rows: List[List[int]] = []
        for row in self.grid:
            is_filled_row = all(cell != self.EMPTY for cell in row)
            if not is_filled_row:
                remaining_rows.append(row)

        cleared = self.height - len(remaining_rows)
        if cleared <= 0:
            return 0

        empty_row = [self.EMPTY for _ in range(self.width)]
        new_rows: List[List[int]] = []
        for _ in range(cleared):
            new_rows.append(empty_row.copy())
        self.grid = new_rows + remaining_rows
        return cleared


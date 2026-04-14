import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
import tkinter
import pygame


# ============================================================
# ViewModel 層: 描画領域ごとの純粋なデータ
# ============================================================

@dataclass
class MatrixViewModel:
    """固定ブロックのみを表す盤面データ"""
    width: int
    height: int
    cells: List[List[int]]   # 0=空, 1=固定ブロック

@dataclass
class ActivePieceViewModel:
    """現在操作中のテトリミノ"""
    blocks: List[tuple]       # 相対座標 List[(bx, by)]
    cell_x: int               # セル座標 X (盤面基準)
    cell_y: int               # セル座標 Y (盤面基準)
    pixel_x: float = 0.0     # ピクセル精度 X (なめらか描画用・将来拡張)
    pixel_y: float = 0.0     # ピクセル精度 Y (なめらか描画用・将来拡張)

@dataclass
class ScoreViewModel:
    """スコア・レベル情報"""
    score: int
    lines: int
    level: int
    goal: int
    game_over: bool

@dataclass
class NextMinoViewModel:
    """次のミノのキュー"""
    kinds: List[str]

# 後方互換: 旧 SampleView が使用する統合 ViewModel
@dataclass
class ViewModel:
    """後方互換のための統合描画データ"""
    width: int
    height: int
    cells: List[List[int]]   # 0=空, >0=ブロック
    score: int
    lines: int
    level: int
    goal: int
    game_over: bool


# ============================================================
# GraphicsAdapter 基底クラス
# ============================================================

class GraphicsAdapter(ABC):
    """グラフィックスアダプタの基底クラス"""

    @abstractmethod
    def begin_frame(self) -> None:
        """フレーム描画開始。内部バッファのクリアや描画準備を行う。"""
        ...

    @abstractmethod
    def draw_matrix(self, vm: MatrixViewModel) -> None:
        """固定ブロック盤面を描画する。"""
        ...

    @abstractmethod
    def draw_active_piece(self, vm: ActivePieceViewModel) -> None:
        """操作中テトリミノを描画する。"""
        ...

    @abstractmethod
    def draw_score(self, vm: ScoreViewModel) -> None:
        """スコア・レベル情報を描画する。"""
        ...

    @abstractmethod
    def draw_next(self, vm: NextMinoViewModel) -> None:
        """次ミノ情報を描画する。"""
        ...

    @abstractmethod
    def end_frame(self) -> None:
        """フレーム描画完了。バッファのフラッシュや画面更新を行う。"""
        ...

    # ----------------------------------------------------------
    # 後方互換: ViewModel を分解して新メソッド群を呼び出す
    # ----------------------------------------------------------
    def render(self, vm: ViewModel) -> None:
        self.begin_frame()
        self.draw_score(ScoreViewModel(
            score=vm.score, lines=vm.lines, level=vm.level,
            goal=vm.goal, game_over=vm.game_over,
        ))
        self.draw_matrix(MatrixViewModel(
            width=vm.width, height=vm.height, cells=vm.cells,
        ))
        self.end_frame()


# ============================================================
# ConsoleGraphicsAdapter
# ============================================================

class ConsoleGraphicsAdapter(GraphicsAdapter):
    """内部バッファを使いフレーム単位でコンソールに描画するアダプタ。
    end_frame() で一括出力することで、画面クリアと描画を1回にまとめる。"""

    EMPTY  = " ."
    FIXED  = "[]"
    ACTIVE = "##"

    def __init__(self):
        self._matrix_vm: Optional[MatrixViewModel] = None
        self._piece_vm:  Optional[ActivePieceViewModel] = None
        self._score_vm:  Optional[ScoreViewModel] = None
        self._next_vm:   Optional[NextMinoViewModel] = None

    def begin_frame(self) -> None:
        self._matrix_vm = None
        self._piece_vm  = None
        self._score_vm  = None
        self._next_vm   = None

    def draw_matrix(self, vm: MatrixViewModel) -> None:
        self._matrix_vm = vm

    def draw_active_piece(self, vm: ActivePieceViewModel) -> None:
        self._piece_vm = vm

    def draw_score(self, vm: ScoreViewModel) -> None:
        self._score_vm = vm

    def draw_next(self, vm: NextMinoViewModel) -> None:
        self._next_vm = vm

    def end_frame(self) -> None:
        """バッファ内容を一括してコンソールに出力する。
        画面クリアを1回だけ呼ぶことでフリッカーを最小化する。"""
        lines: List[str] = []

        if self._score_vm:
            sv = self._score_vm
            lines.append(
                f"SCORE: {sv.score}   LINES: {sv.lines}   "
                f"LEVEL: {sv.level}   GOAL: {sv.goal}"
            )

        if self._matrix_vm:
            mv = self._matrix_vm
            # 固定ブロックに操作中ミノをセル座標でオーバーレイ
            merged = [row[:] for row in mv.cells]
            if self._piece_vm:
                pv = self._piece_vm
                for bx, by in pv.blocks:
                    x = pv.cell_x + bx
                    y = pv.cell_y + by
                    if 0 <= y < mv.height and 0 <= x < mv.width:
                        merged[y][x] = 2

            lines.append("+" + "--" * mv.width + "+")
            for row in merged:
                line = "|"
                for cell in row:
                    if cell == 0:
                        line += self.EMPTY
                    elif cell == 1:
                        line += self.FIXED
                    else:
                        line += self.ACTIVE
                line += "|"
                lines.append(line)
            lines.append("+" + "--" * mv.width + "+")

        if self._next_vm and self._next_vm.kinds:
            lines.append("NEXT: " + ", ".join(self._next_vm.kinds))

        if self._score_vm and self._score_vm.game_over:
            lines.append("=== GAME OVER ===")

        self._clear_screen()
        print("\n".join(lines))

    @staticmethod
    def _clear_screen() -> None:
        os.system("cls" if os.name == "nt" else "clear")


# ============================================================
# TkinterGraphicsAdapter
# ============================================================

class TkinterGraphicsAdapter(GraphicsAdapter):
    """内部バッファを使いフレーム単位で tkinter Canvas に描画するアダプタ。"""

    EMPTY  = " ."
    FIXED  = "[]"
    ACTIVE = "##"

    def __init__(self, root: tkinter.Tk):
        # root は Platform から DI される
        canvas = tkinter.Canvas(root, width=400, height=600)
        canvas.pack()
        self.canvas = canvas
        self._matrix_vm: Optional[MatrixViewModel] = None
        self._piece_vm:  Optional[ActivePieceViewModel] = None
        self._score_vm:  Optional[ScoreViewModel] = None
        self._next_vm:   Optional[NextMinoViewModel] = None

    def begin_frame(self) -> None:
        self._matrix_vm = None
        self._piece_vm  = None
        self._score_vm  = None
        self._next_vm   = None

    def draw_matrix(self, vm: MatrixViewModel) -> None:
        self._matrix_vm = vm

    def draw_active_piece(self, vm: ActivePieceViewModel) -> None:
        self._piece_vm = vm

    def draw_score(self, vm: ScoreViewModel) -> None:
        self._score_vm = vm

    def draw_next(self, vm: NextMinoViewModel) -> None:
        self._next_vm = vm

    def end_frame(self) -> None:
        lines: List[str] = []

        if self._score_vm:
            sv = self._score_vm
            lines.append(f"SCORE: {sv.score}   LINES: {sv.lines}")
            lines.append(f"LEVEL: {sv.level}   GOAL: {sv.goal}")

        if self._matrix_vm:
            mv = self._matrix_vm
            merged = [row[:] for row in mv.cells]
            if self._piece_vm:
                pv = self._piece_vm
                for bx, by in pv.blocks:
                    x = pv.cell_x + bx
                    y = pv.cell_y + by
                    if 0 <= y < mv.height and 0 <= x < mv.width:
                        merged[y][x] = 2

            lines.append("+" + "--" * mv.width + "+")
            for row in merged:
                line = "|"
                for cell in row:
                    if cell == 0:
                        line += self.EMPTY
                    elif cell == 1:
                        line += self.FIXED
                    else:
                        line += self.ACTIVE
                line += "|"
                lines.append(line)
            lines.append("+" + "--" * mv.width + "+")

        if self._next_vm and self._next_vm.kinds:
            lines.append("NEXT: " + ", ".join(self._next_vm.kinds))

        if self._score_vm and self._score_vm.game_over:
            lines.append("=== GAME OVER ===")

        self.canvas.delete("all")
        self.canvas.create_text(0, 0, anchor="nw", text="\n".join(lines), font=("Courier",))


# ============================================================
# PygameGraphicsAdapter
# ============================================================
class PygameGraphicsAdapter(GraphicsAdapter):
    """ViewModel を受け取って Pygame に描画する"""

    BLOCK_WIDTH = 20
    BLOCK_HEIGHT = 20

    def __init__(self, screen: pygame.surface):
        self.screen = screen
        self._matrix_vm: Optional[MatrixViewModel] = None
        self._piece_vm:  Optional[ActivePieceViewModel] = None
        self._score_vm:  Optional[ScoreViewModel] = None
        self._next_vm:   Optional[NextMinoViewModel] = None

    def begin_frame(self) -> None:
        self._matrix_vm = None
        self._piece_vm  = None
        self._score_vm  = None
        self._next_vm   = None

    def draw_matrix(self, vm: MatrixViewModel) -> None:
        self._matrix_vm = vm

    def draw_active_piece(self, vm: ActivePieceViewModel) -> None:
        self._piece_vm = vm

    def draw_score(self, vm: ScoreViewModel) -> None:
        self._score_vm = vm

    def draw_next(self, vm: NextMinoViewModel) -> None:
        self._next_vm = vm

    def end_frame(self) -> None:
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 24)
        if self._score_vm:
            score_text = font.render(f"SCORE: {self._score_vm.score}   LINES: {self._score_vm.lines}   LEVEL: {self._score_vm.level}   GOAL: {self._score_vm.goal}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 450))
        
        if self._matrix_vm:
            for rowindex, row in enumerate(self._matrix_vm.cells):
                for colindex, cell in enumerate(row):
                    if cell == 0:
                        block = pygame.Rect(
                            self.BLOCK_WIDTH * colindex,
                            self.BLOCK_HEIGHT * rowindex,
                            self.BLOCK_WIDTH - 1,
                            self.BLOCK_HEIGHT - 1)
                        pygame.draw.rect(self.screen, (255, 255, 255), block)
                    elif cell == 1:
                        block = pygame.Rect(
                            self.BLOCK_WIDTH * colindex,
                            self.BLOCK_HEIGHT * rowindex,
                            self.BLOCK_WIDTH - 1,
                            self.BLOCK_HEIGHT - 1)
                        pygame.draw.rect(self.screen, (0, 255, 0), block)
                    else:
                        block = pygame.Rect(
                            self.BLOCK_WIDTH * colindex,
                            self.BLOCK_HEIGHT * rowindex,
                            self.BLOCK_WIDTH - 1,
                            self.BLOCK_HEIGHT - 1)
                        pygame.draw.rect(self.screen, (255, 0, 0), block)
        if self._score_vm and self._score_vm.game_over:
            message_text = font.render("=== GAME OVER ===", True, (255, 255, 255))
            self.screen.blit(message_text, (10, 500))
        pygame.display.flip()


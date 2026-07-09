from typing import List

from SimpleTetris.GameLogicMatrix.GameLogicMatrixModel import GameLogicMatrixModel
from SimpleTetris.GameLogicTetrimino.GameLogicTetriminoModel import Tetrimino, Point, TETRIMINO_KINDS

class GameModel:
    matrix: GameLogicMatrixModel
    active_piece: Tetrimino
    active_pos: Point
    next_queue: List[str]
    score: int = 0
    lines: int = 0
    level: int = 1
    goal: int = 10
    game_over: bool = False
    drop_delta: int = 0

    # Level → Fall Speed（ミリ秒）インデックス 0 は未使用
    FALL_SPEED_MS = (
        1000,  # level 0 (unused)
        1000,  # level 1
         793,  # level 2
         618,  # level 3
         473,  # level 4
         355,  # level 5
         262,  # level 6
         190,  # level 7
         135,  # level 8
          94,  # level 9
          64,  # level 10
          43,  # level 11
          28,  # level 12
          18,  # level 13
          11,  # level 14
           7,  # level 15
    )

    def __init__(self, matrix: GameLogicMatrixModel, active_piece: Tetrimino, active_pos: Point, next_queue: List[str]):
        self.matrix = matrix
        self.active_piece = active_piece
        self.last_lockdown_piece = active_piece
        self.active_pos = active_pos
        self.last_lockdown_pos = active_pos
        self.next_queue = next_queue
        self.score = 0
        self.lines = 0
        self.level = 1
        self.goal = 10
        self.game_over = False
        self.last_lines_cleared = 0

    def is_GameOver(self):
        return self.game_over
    
    def get_fall_speed_ms(self) -> int:
        # Level を指定して Fall Speed（ミリ秒）を取得する。
        # 定義外の Level の場合は 1000 を返す。
        if 1 <= self.level < len(self.FALL_SPEED_MS):
            return self.FALL_SPEED_MS[self.level]
        return 1000

    @staticmethod
    def initial(width: int = 10, height: int = 20) -> "GameModel":
        matrix = GameLogicMatrixModel(width, height)
        queue = []
        kind = TETRIMINO_KINDS[0]  # 最初のテトリミノはIにする
        active = Tetrimino(kind)
        pos = (3, 0)  # 左から3に湧く
        return GameModel(matrix, active, pos, queue)

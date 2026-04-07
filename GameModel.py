from typing import List

from SimpleTetris.domain import Matrix, Tetromino, TETROMINO_KINDS, Point, shuffled_bag


class GameModel:
    matrix: Matrix
    active_piece: Tetromino
    active_pos: Point
    next_queue: List[str]
    score: int = 0
    lines: int = 0
    level: int = 1
    goal: int = 10
    game_over: bool = False

    # Level → Fall Speed（ミリ秒）
    FALL_SPEED_MS = {
        1: 1000,
        2: 793,
        3: 618,
        4: 473,
        5: 355,
        6: 262,
        7: 190,
        8: 135,
        9: 94,
        10: 64,
        11: 43,
        12: 28,
        13: 18,
        14: 11,
        15: 7,
    }

    def __init__(self, matrix: Matrix, active_piece: Tetromino, active_pos: Point, next_queue: List[str]):
        self.matrix = matrix
        self.active_piece = active_piece
        self.active_pos = active_pos
        self.next_queue = next_queue

    def is_GameOver(self):
        return self.game_over
    
    def get_fall_speed_ms(self) -> int:
        # Levelを指定してFall Speed（ミリ秒）を取得する。
        # 定義外のLevelの場合は 1000 を返す。
        return self.FALL_SPEED_MS.get(self.level, 1000)

    @staticmethod
    def initial(width: int = 10, height: int = 20) -> "GameModel":
        matrix = Matrix(width, height)
        queue = shuffled_bag()
        kind = queue.pop()
        active = Tetromino(kind)
        pos = (3, 0)  # 左から3に湧く
        return GameModel(matrix, active, pos, queue)

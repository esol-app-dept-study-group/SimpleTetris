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
    game_over: bool = False

    def __init__(self, matrix: Matrix, active_piece: Tetromino, active_pos: Point, next_queue: List[str]):
        self.matrix = matrix
        self.active_piece = active_piece
        self.active_pos = active_pos
        self.next_queue = next_queue

    def is_GameOver(self):
        return self.game_over

    @staticmethod
    def initial(width: int = 10, height: int = 20) -> "GameModel":
        matrix = Matrix(width, height)
        queue = shuffled_bag()
        kind = queue.pop()
        active = Tetromino(kind)
        pos = (3, 0)  # 左から3に湧く
        return GameModel(matrix, active, pos, queue)

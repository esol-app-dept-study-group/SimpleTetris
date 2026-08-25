from SimpleTetris.TetriminoDef import TetriminoType
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

Point = Tuple[int, int]  # (x, y)

# 4x4 内のブロック座標を回転ごとに定義
TETRIMINO_SHAPES: Dict[str, List[List[Point]]] = {
    "I": [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(1, 0), (1, 1), (1, 2), (1, 3)],
    ],
    "O": [
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
    ],
    "T": [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(1, 1), (2, 1), (0, 2), (1, 2)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
    ],
}

TETRIMINO_KINDS = list(TETRIMINO_SHAPES.keys())

TETRIMINO_DEFAULT_FALL_POS = {
    'I': (4, 0),
    'O': (5, 0),
    'T': (4, 0),
    'J': (4, 0),
    'L': (4, 0),
    'S': (4, 0),
    'Z': (4, 0),
}

class GameLogicTetriminoModel:
    CurrentMino: TetriminoType
    x: int
    y: int
    """テトリミノのロジックを管理するクラス"""
    def __init__(self):
        pass

@dataclass
class Tetrimino:
    kind: str
    rotation: int = 0  # 0始まり

    def blocks(self) -> List[Point]:
        """原点(0,0)からのブロック相対座標を返す"""
        return TETRIMINO_SHAPES[self.kind][self.rotation % 4]

    def rotated(self, delta: int) -> "Tetrimino":
        return Tetrimino(self.kind, (self.rotation + delta) % 4)

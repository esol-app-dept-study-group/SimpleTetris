import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

Point = Tuple[int, int]  # (x, y)

# 4x4 内のブロック座標を回転ごとに定義
TETROMINO_SHAPES: Dict[str, List[List[Point]]] = {
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

TETROMINO_KINDS = list(TETROMINO_SHAPES.keys())


@dataclass
class Tetromino:
    kind: str
    rotation: int = 0  # 0始まり

    def blocks(self) -> List[Point]:
        """原点(0,0)からのブロック相対座標を返す"""
        return TETROMINO_SHAPES[self.kind][self.rotation % 4]

    def rotated(self, delta: int) -> "Tetromino":
        return Tetromino(self.kind, (self.rotation + delta) % 4)


@dataclass
class Matrix:
    width: int = 10
    height: int = 20
    cells: List[List[int]] = field(default_factory=list)  # 0=空, >0=色ID

    def __post_init__(self):
        if not self.cells:
            self.cells = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_empty(self, x: int, y: int) -> bool:
        return self.in_bounds(x, y) and self.cells[y][x] == 0

    def can_place(self, piece: Tetromino, pos: Point) -> bool:
        px, py = pos
        for bx, by in piece.blocks():
            x = px + bx
            y = py + by
            if not self.in_bounds(x, y) or self.cells[y][x] != 0:
                return False
        return True

    def lock(self, piece: Tetromino, pos: Point, color_id: int) -> None:
        px, py = pos
        for bx, by in piece.blocks():
            x = px + bx
            y = py + by
            if self.in_bounds(x, y):
                self.cells[y][x] = color_id

    def clear_lines(self) -> int:
        """埋まった行を消し、クリアした行数を返す"""
        new_rows = [row for row in self.cells if 0 in row]
        cleared = self.height - len(new_rows)
        while len(new_rows) < self.height:
            new_rows.insert(0, [0 for _ in range(self.width)])
        self.cells = new_rows
        return cleared


def shuffled_bag() -> List[str]:
    """テトリミノの7種1セットをシャッフルして返す"""
    bag = TETROMINO_KINDS.copy()
    random.shuffle(bag)
    return bag

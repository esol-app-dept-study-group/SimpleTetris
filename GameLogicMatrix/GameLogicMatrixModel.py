from SimpleTetris.TetriminoDef import TetriminoType
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from SimpleTetris.GameLogicTetrimino.GameLogicTetriminoModel import Tetrimino, Point

@dataclass
class GameLogicMatrixModel:
    width: int = 10
    height: int = 20
    grid: List[List[int]] = field(default_factory=list)  # 0=ãÛ, >0=êFID

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
        self.width = width
        self.height = height
        self.grid = [[self.EMPTY for _ in range(self.width)] for _ in range(self.height)]


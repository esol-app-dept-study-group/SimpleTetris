import os
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional

# ============================================================
# アダプタ層: グラフィックス/UI（コンソール）
# ============================================================

@dataclass
class ViewModel:
    """描画アダプタに渡すための純粋なデータ"""
    width: int
    height: int
    cells: List[List[int]]  # 0=空, >0=ブロック
    score: int
    lines: int
    level: int
    game_over: bool

class ConsoleGraphicsAdapter:
    """ViewModel を受け取ってコンソールに描画する"""

    EMPTY = " ."
    FIXED = "[]"
    ACTIVE = "##"

    def render(self, vm: ViewModel) -> None:
        self._clear_screen()
        print(f"SCORE: {vm.score}   LINES: {vm.lines}   LEVEL: {vm.level}")
        print("+" + "--" * vm.width + "+")
        for row in vm.cells:
            line = "|"
            for cell in row:
                if cell == 0:
                    line += self.EMPTY
                elif cell == 1:
                    line += self.FIXED
                else:
                    line += self.ACTIVE
            line += "|"
            print(line)
        print("+" + "--" * vm.width + "+")
        if vm.game_over:
            print("=== GAME OVER ===")

    @staticmethod
    def _clear_screen():
        # 簡易画面クリア（環境によっては効かない場合もある）
        os.system("cls" if os.name == "nt" else "clear")


class GraphicsAdapter:
    def __init__(self):
        self.core = ConsoleGraphicsAdapter()
    
    def render(self, vm: ViewModel) -> None:
        self.core.render(vm)

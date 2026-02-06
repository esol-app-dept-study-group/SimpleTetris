from SimpleTetris.view_base import ViewBase
from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.GraphicsAdapter import GraphicsAdapter, ViewModel

class SampleView(ViewBase):
    def __init__(self):
        self.gfx = GraphicsAdapter()
    def __call__(self, state: GameModel):
        # 固定ブロック＋落下中ピースを合成した一時ボードを作る
        tmp = [row[:] for row in state.matrix.cells]
        px, py = state.active_pos
        for bx, by in state.active_piece.blocks():
            x = px + bx
            y = py + by
            if 0 <= y < state.matrix.height and 0 <= x < state.matrix.width:
                tmp[y][x] = 2  # 操作中ピースは 2 として区別

        vm = ViewModel(
            width=state.matrix.width,
            height=state.matrix.height,
            cells=tmp,
            score=state.score,
            lines=state.lines,
            level=state.level,
            game_over=state.game_over,
        )
        # GraphicsAdapter のAPIコール
        self.gfx.render(vm)

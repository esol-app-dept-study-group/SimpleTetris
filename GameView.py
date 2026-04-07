from SimpleTetris.sample.SampleView import SampleView
from SimpleTetris.view_base import ViewBase
from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.GraphicsAdapter import GraphicsAdapter


class GameView:
    def __init__(self, gfx: GraphicsAdapter = None):
        self.subViewList = [SampleView(gfx)]

    def __call__(self, state: GameModel):
        for view in self.subViewList:
            state = view(state)
        return state

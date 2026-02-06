from SimpleTetris.sample.SampleView import SampleView
from SimpleTetris.view_base import ViewBase
from SimpleTetris.GameModel import GameModel


class GameView:
    def __init__(self):
        self.subViewList = [SampleView()]

    def __call__(self, state: GameModel):
        for view in self.subViewList:
            return view(state)

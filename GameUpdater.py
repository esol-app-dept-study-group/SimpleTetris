from SimpleTetris.updater_base import UpdaterBase
from SimpleTetris.sample.SampleUpdater import SampleUpdater
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus
from SimpleTetris.GameModel import GameModel
from SimpleTetris.GameLogicLevel.GameLogicLevelUpdater import GameLogicLevelUpdater


class GameUpdater:
    def __init__(self):
        self.subUpdaterList = [
            SampleUpdater(),
            GameLogicLevelUpdater(),
        ]

    def __call__(self, state: GameModel, event: EventBus) -> GameModel:
        for updater in self.subUpdaterList:
            state = updater(state, event)
        return state

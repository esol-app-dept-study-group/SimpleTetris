from SimpleTetris.updater_base import UpdaterBase
from SimpleTetris.sample.SampleUpdater import SampleUpdater
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus
from SimpleTetris.GameModel import GameModel


class GameUpdater:
    def __init__(self):
        self.subUpdaterList = [SampleUpdater()]

    def __call__(self, state: GameModel, event: EventBus) -> GameModel:
        for updater in self.subUpdaterList:
            return updater(state, event)

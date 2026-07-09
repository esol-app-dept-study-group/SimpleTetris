from SimpleTetris.updater_base import UpdaterBase
from SimpleTetris.sample.SampleUpdater import SampleUpdater
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus
from SimpleTetris.GameModel import GameModel
from SimpleTetris.GameLogicLevel.GameLogicLevelUpdater import GameLogicLevelUpdater
from SimpleTetris.GameLogicTetrimino.GameLogicTetriminoUpdater import GameLogicTetriminoUpdater
from SimpleTetris.GameLogicNextMino.GameLogicNextMinoUpdater import GameLogicNextMinoUpdater
from SimpleTetris.GameLogicMatrix.GameLogicMatrixUpdater import GameLogicMatrixUpdater
from SimpleTetris.GameLogicScore.GameLogicScoreUpdater import GameLogicScoreUpdater

class GameUpdater:
    def __init__(self):
        self.subUpdaterList = [
            GameLogicLevelUpdater(),
            GameLogicNextMinoUpdater(),
            GameLogicTetriminoUpdater(),
            GameLogicMatrixUpdater(),
            GameLogicScoreUpdater(),
        ]

    def __call__(self, state: GameModel, event: EventBus) -> GameModel:
        for updater in self.subUpdaterList:
            state = updater(state, event, updater._compute_elapsed_ms())
        return state

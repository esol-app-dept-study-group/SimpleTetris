from SimpleTetris.updater_base import UpdaterBase
from SimpleTetris.eventdef import GameEvent
from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus

class GameLogicTetriminoUpdater(UpdaterBase):
    def __call__(self, state: GameModel, event: EventBus, elapsed_time:float) -> GameModel:
        for ev in event.poll():
            if (ev == GameEvent.INPUTEVENT_INITIALIZED) or (ev == GameEvent.INPUTEVENT_TETRIMINO_LOCKDOWN):
                # 新しいテトリミノを生成して、落下開始位置に置く
                self.create_new_piece(state)
        return state

    """
    新規のテトリミノを生成して、落下開始位置に置く。
    """
    def create_new_piece(self, state: GameModel) -> GameModel:
        # NextMino から新しいテトリミノの種類を取り出して
        # 
        return state

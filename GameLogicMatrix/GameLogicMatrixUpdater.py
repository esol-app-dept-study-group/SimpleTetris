from SimpleTetris.updater_base import UpdaterBase
from SimpleTetris.eventdef import GameEvent
from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus

class GameLogicMatrixUpdater(UpdaterBase):
    def __call__(self, state: GameModel, event: EventBus, elapsed_time:float) -> GameModel:
        if event.has_event(GameEvent.INPUTEVENT_MINO_DROPED):
            # 新しいテトリミノを落下開始位置に置く
            pass
            # ラインが埋まったか判定し、埋まっていたら
            # そのラインをクリアして GameEvent.INPUTEVENT_LINE_CLEARED を通知する
            pass
            # Lockdownを通知する
            pass

        return state
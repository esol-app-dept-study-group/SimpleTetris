
from SimpleTetris.updater_base import UpdaterBase
from SimpleTetris.eventdef import GameEvent
from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus
from SimpleTetris.GameLogicTetrimino.GameLogicTetriminoModel import Tetrimino, Point

class GameLogicScoreUpdater(UpdaterBase):
    def __call__(self, state: GameModel, event: EventBus, elapsed_time:float) -> GameModel:
        if event.has_event(GameEvent.INPUTEVENT_TETRIMINO_LOCKDOWN) and event.has_event(GameEvent.INPUTEVENT_HARD_DROP):
            # Hard Drop で Lockdown した場合、スコアを加算する
            pass
        elif event.has_event(GameEvent.INPUTEVENT_TETRIMINO_LOCKDOWN) and event.has_event(GameEvent.INPUTEVENT_LINE_CLEARED):
            # Lockdown かつ LINE_CLEARED なら、消えたライン分をスコアに加算する
            pass
        return state
    

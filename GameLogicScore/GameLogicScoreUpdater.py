
from SimpleTetris.updater_base import UpdaterBase
from SimpleTetris.eventdef import GameEvent
from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus

class GameLogicScoreUpdater(UpdaterBase):
    def __call__(self, state: GameModel, event: EventBus, elapsed_time:float) -> GameModel:
        if event.has_event(GameEvent.INPUTEVENT_TETRIMINO_LOCKDOWN) and event.has_event(GameEvent.INPUTEVENT_HARD_DROP):
            # Hard Drop で Lockdown した場合、スコアを加算する.
            state.score += self.calc_score_hard_drop(state)
            pass
        elif event.has_event(GameEvent.INPUTEVENT_TETRIMINO_LOCKDOWN) and event.has_event(GameEvent.INPUTEVENT_LINE_CLEARED):
            # Lockdown かつ LINE_CLEARED なら、消えたライン分をスコアに加算する.
            state.score += self.calc_score_line_cleared(state)
            pass
        return state
    
    # Hard Dropでロックダウンした時のスコアを計算する関数.
    def calc_score_hard_drop(self, state: GameModel) -> int:
        ret = state.drop_delta * 2
        return ret
    
    # 現在のレベルと消えたライン数に応じてスコアを返す関数.
    def calc_score_line_cleared(self, state: GameModel) -> int:
        match state.last_lines_cleared:
            case 1:
                return 100 * state.level
            case 2:
                return 300 * state.level
            case 3:
                return 500 * state.level
            case 4:
                return 800 * state.level
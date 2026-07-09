from SimpleTetris.updater_base import UpdaterBase
from SimpleTetris.eventdef import GameEvent
from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus

# ゲームレベルの最大は15
GAME_LEVEL_MAX = 15

# 10ラインクリアごとにレベルが1上がる
GAME_LEVEL_UP_LINES = 10

class GameLogicLevelUpdater(UpdaterBase):
    def __call__(self, state: GameModel, event: EventBus, elapsed_time:float) -> GameModel:
        if event.has_event(GameEvent.INPUTEVENT_TETRIMINO_LOCKDOWN) and event.has_event(GameEvent.INPUTEVENT_LINE_CLEARED):
            # Lockdown したら、次のテトリミノを生成するイベントを発行する
                # 【仮実装】実際はラインクリアのイベントが来ると思うがTICKでお試し。
                calculated_level = (state.lines // GAME_LEVEL_UP_LINES) + 1
            state.lines += state.last_lines_cleared
                state.level = min(calculated_level, GAME_LEVEL_MAX)
                state.goal = GAME_LEVEL_UP_LINES - (state.lines % GAME_LEVEL_UP_LINES)
            event.emit(GameEvent.INPUTEVENT_LEVEL_UPDATED)
        return state

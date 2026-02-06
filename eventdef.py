from enum import Enum, auto

class GameEvent(Enum):
    """Updater に送るメッセージ（入力などの抽象化）"""
    INPUTEVENT_TICK = auto()
    INPUTEVENT_LEFT = auto()
    INPUTEVENT_RIGHT = auto()
    INPUTEVENT_ROTATE = auto()
    INPUTEVENT_SOFT_DROP = auto()
    INPUTEVENT_HARD_DROP = auto()
    INPUTEVENT_QUIT = auto()


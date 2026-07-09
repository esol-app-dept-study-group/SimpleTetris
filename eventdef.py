from enum import Enum, auto

class GameEvent(Enum):
    """Updater に送るメッセージ（入力などの抽象化）"""
    INPUTEVENT_INITIALIZED = auto()         # ゲーム開始時に一度だけ送られるイベント
    INPUTEVENT_TICK = auto()
    INPUTEVENT_LEFT = auto()
    INPUTEVENT_RIGHT = auto()
    INPUTEVENT_ROTATE = auto()
    INPUTEVENT_SOFT_DROP = auto()
    INPUTEVENT_HARD_DROP = auto()
    INPUTEVENT_QUIT = auto()
    INPUTEVENT_LINE_CLEARED = auto()        # ラインがクリアされたときに送られるイベント
    INPUTEVENT_TETRIMINO_LOCKDOWN = auto()  # テトリミノがロックダウンしたときに送られるイベント
    INPUTEVENT_MINO_DROPED = auto()    # 新しいテトリミノが生成されたときに送られるイベント
    INPUTEVENT_NEXT_MINO_REFILLED = auto()  # ネクストミノが補充されたときに送られるイベント
    INPUTEVENT_SCORE_UPDATED = auto()          # スコアが更新されたときに送られるイベント
    INPUTEVENT_LEVEL_UPDATED = auto()          # レベルが更新されたときに送られるイベント
    INPUTEVENT_GAME_OVER = auto()          # ゲームオーバーになったときに送られるイベント


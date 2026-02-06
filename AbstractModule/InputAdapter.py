from SimpleTetris.eventdef import GameEvent

# ============================================================
# アダプタ層: 入力（コンソール）
# ============================================================

class ConsoleInputAdapter:
    """
    実際の入力を読み取り、Command に変換する。
    - a: 左
    - d: 右
    - w: 回転
    - s: ソフトドロップ
    - space: ハードドロップ
    - q: 終了
    何も入力せず Enter なら TICK として扱う。
    """

    def get_event(self) -> GameEvent:
        s = input("Command (a/d/w/s/space/q, Enter=tick): ").strip().lower()
        if s == "a":
            return GameEvent.INPUTEVENT_LEFT
        if s == "d":
            return GameEvent.INPUTEVENT_RIGHT
        if s == "w":
            return GameEvent.INPUTEVENT_ROTATE
        if s == "s":
            return GameEvent.INPUTEVENT_SOFT_DROP
        if s == " " or s == "space":
            return GameEvent.INPUTEVENT_HARD_DROP
        if s == "q":
            return GameEvent.INPUTEVENT_QUIT
        return GameEvent.INPUTEVENT_TICK


class InputAdapter:
    def __init__(self):
        self.core = ConsoleInputAdapter()
    def get_event(self) -> GameEvent:
        return self.core.get_event()

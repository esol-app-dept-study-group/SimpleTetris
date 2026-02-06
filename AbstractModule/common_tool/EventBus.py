from collections import deque
from typing import Deque, Iterable

from SimpleTetris.eventdef import GameEvent


class EventBus:
    """Tick 単位でイベントを受け渡すキュー."""

    def __init__(self) -> None:
        # _current_tick: 前 tick で発生したイベント（今 tick で読む）
        # _next_tick: 今 tick 中に発生したイベント（次 tick で読む）
        self._current_tick: Deque[GameEvent] = deque()
        self._next_tick: Deque[GameEvent] = deque()

    def emit(self, event: GameEvent) -> None:
        """今 tick 中に発生したイベントを次 tick 用キューに積む."""
        self._next_tick.append(event)

    def poll(self) -> Iterable[GameEvent]:
        """前 tick で積まれたイベントを読み取る."""
        return tuple(self._current_tick)

    def end_tick(self) -> None:
        """tick 終了処理: 今 tick のイベントを次 tick にスワップし、古いものを捨てる."""
        self._current_tick.clear()
        self._current_tick, self._next_tick = self._next_tick, self._current_tick
        self._next_tick.clear()

    def clear_all(self) -> None:
        """すべてのキューを空にする（リセット用）."""
        self._current_tick.clear()
        self._next_tick.clear()

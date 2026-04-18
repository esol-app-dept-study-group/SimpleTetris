from time import perf_counter
from abc import ABC, abstractmethod

from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus


class UpdaterBase(ABC):
    def __init__(self):
            self.last_called = None

    """
    内部向けAPI.
    前回この updater が呼ばれてからの経過時間をミリ秒で返す。

    NOTE:
    Pythonには protected 修飾子がないため、先頭に _ を付けている。
    フレームワーク内部 (GameUpdater) からの使用を想定。
    """
    def _compute_elapsed_ms(self):
        now = perf_counter()
        if self.last_called is None:
            elapsed = 0.0
        else:
            elapsed = (now - self.last_called) * 1000  # ms
        self.last_called = now
        return elapsed
    
    @abstractmethod
    def __call__(self, state: GameModel, cmd: EventBus, elapsed_time:float) -> GameModel:
        """1 tick 分のイベント処理を行い、新しい状態を返す"""
        raise NotImplementedError

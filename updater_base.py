from abc import ABC, abstractmethod

from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus


class UpdaterBase(ABC):
    @abstractmethod
    def __call__(self, state: GameModel, cmd: EventBus) -> GameModel:
        """1 tick 分のイベント処理を行い、新しい状態を返す"""
        raise NotImplementedError

from abc import ABC, abstractmethod

from SimpleTetris.GameModel import GameModel


class ViewBase(ABC):
    @abstractmethod
    def __call__(self, state: GameModel):
        raise NotImplementedError

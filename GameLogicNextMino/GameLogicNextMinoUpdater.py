from SimpleTetris.updater_base import UpdaterBase
from SimpleTetris.eventdef import GameEvent
from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus
from SimpleTetris.GameLogicNextMino.NextMinoPermutation import get_random_permutation


class GameLogicNextMinoUpdater(UpdaterBase):

    def __call__(self, state: GameModel, event: EventBus, elapsed_time:float) -> GameModel:
        # ネクストミノが7以下になったら7つミノを補充する
        self.refill_mino(state)
        return state

    def refill_mino(self, state: GameModel) -> None:
        if len(state.next_queue) < 7:
            next_minos = get_random_permutation()
            state.next_queue.extend(mino.name for mino in next_minos)

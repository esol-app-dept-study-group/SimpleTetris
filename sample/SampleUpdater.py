import random

from SimpleTetris.updater_base import UpdaterBase
from SimpleTetris.eventdef import GameEvent
from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus
from SimpleTetris.domain import Tetromino, TETROMINO_KINDS


class SampleUpdater(UpdaterBase):
    def __call__(self, state: GameModel, event: EventBus) -> GameModel:
        for ev in event.poll():
            if ev == GameEvent.INPUTEVENT_QUIT:
                state.game_over = True
                return state

            if state.game_over:
                return state

            if ev == GameEvent.INPUTEVENT_LEFT:
                self._try_move(state, dx=-1, dy=0)
            elif ev == GameEvent.INPUTEVENT_RIGHT:
                self._try_move(state, dx=+1, dy=0)
            elif ev == GameEvent.INPUTEVENT_ROTATE:
                self._try_rotate(state)
            elif ev == GameEvent.INPUTEVENT_SOFT_DROP:
                self._try_move(state, dx=0, dy=1)
            elif ev == GameEvent.INPUTEVENT_HARD_DROP:
                self._hard_drop(state)
            elif ev == GameEvent.INPUTEVENT_TICK:
                moved = self._try_move(state, dx=0, dy=1)
                if not moved:
                    self._lock_and_spawn(state)

        return state

    # ---- 以下は内部ヘルパー（ドメイン操作） ----

    def _try_move(self, state: GameModel, dx: int, dy: int) -> bool:
        x, y = state.active_pos
        new_pos = (x + dx, y + dy)
        if state.matrix.can_place(state.active_piece, new_pos):
            state.active_pos = new_pos
            return True
        return False

    def _try_rotate(self, state: GameModel) -> None:
        rotated = state.active_piece.rotated(+1)
        if state.matrix.can_place(rotated, state.active_pos):
            state.active_piece = rotated

    def _hard_drop(self, state: GameModel) -> None:
        while self._try_move(state, dx=0, dy=1):
            pass
        self._lock_and_spawn(state)

    def _lock_and_spawn(self, state: GameModel) -> None:
        state.matrix.lock(state.active_piece, state.active_pos, color_id=1)
        cleared = state.matrix.clear_lines()
        if cleared > 0:
            state.lines += cleared
            state.score += cleared * 100

        next_kind = self._next_kind(state)
        state.active_piece = Tetromino(next_kind)
        state.active_pos = (3, 0)
        if not state.matrix.can_place(state.active_piece, state.active_pos):
            state.game_over = True

    def _next_kind(self, state: GameModel) -> str:
        if not state.next_queue:
            state.next_queue = TETROMINO_KINDS.copy()
            random.shuffle(state.next_queue)
        return state.next_queue.pop()

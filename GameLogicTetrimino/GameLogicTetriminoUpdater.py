from SimpleTetris.updater_base import UpdaterBase
from SimpleTetris.eventdef import GameEvent
from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus
from SimpleTetris.GameLogicTetrimino.GameLogicTetriminoModel import TETRIMINO_DEFAULT_FALL_POS, Tetrimino   

class GameLogicTetriminoUpdater(UpdaterBase):
    def __init__(self):
        self._C_MOVE_LEFT_X_DELTA = -1
        self._C_MOVE_RIGHT_X_DELTA = 1
        self._C_MOVE_DROP_Y_DELTA = 1
        self._drop_accumulator_ms = 0.0
        super().__init__()

    def __call__(self, state: GameModel, event: EventBus, elapsed_time:float) -> GameModel:
        for ev in event.poll():
            result = None
            if ev == GameEvent.INPUTEVENT_INITIALIZED:
                # 新しいテトリミノを生成して、落下開始位置に置く
                self.create_new_piece(state)
            elif ev == GameEvent.INPUTEVENT_LINE_CLEARED:
                # ラインがクリアされたときは、テトリミノの位置を変えない（ただし、ロックダウンしているテトリミノは消える）
                pass
            elif ev in [GameEvent.INPUTEVENT_LEFT, GameEvent.INPUTEVENT_RIGHT, GameEvent.INPUTEVENT_SOFT_DROP, GameEvent.INPUTEVENT_HARD_DROP]:
                # キー入力に従ってテトリミノを移動・回転させる
                result = self.move_piece(state, ev, elapsed_time)
            elif ev == GameEvent.INPUTEVENT_TICK:
                # elapsed_time を積算し、レベルのドロップ速度に達したときだけ落下させる
                self._drop_accumulator_ms += elapsed_time
                fall_speed_ms = state.get_fall_speed_ms()
                if self._drop_accumulator_ms >= fall_speed_ms:
                    self._drop_accumulator_ms -= fall_speed_ms
                    result = self.move_piece(state, ev, elapsed_time)
            elif ev == GameEvent.INPUTEVENT_ROTATE:
                self.rotate_piece(state)
            elif ev == GameEvent.INPUTEVENT_QUIT:
                state.game_over = True
            # Lockdownしたか？
            if result == GameEvent.INPUTEVENT_NEW_ACTIVE_MINO_CREATED:
                # Lockdown したら、テトリミノ生成済みイベント発行し、Matrix の更新を行う
                event.emit(GameEvent.INPUTEVENT_NEW_ACTIVE_MINO_CREATED)
                
        return state

    """
    新規のテトリミノを生成して、落下開始位置に置く。
    """
    def create_new_piece(self, state: GameModel) -> None:
        # NextMino から新しいテトリミノの種類を取り出して初期位置に設置
        tetromino_kind = state.next_queue.pop()
        state.active_piece = Tetrimino(tetromino_kind)
        state.active_pos = TETRIMINO_DEFAULT_FALL_POS[tetromino_kind]

    """
    キー入力に従ってテトリミノを移動させる。
        GameEvent.INPUTEVENT_LEFT
        GameEvent.INPUTEVENT_RIGHT
        GameEvent.INPUTEVENT_SOFT_DROP
        GameEvent.INPUTEVENT_HARD_DROP
        GameEvent.INPUTEVENT_TICK
    """
    def move_piece(self, state: GameModel, ev: GameEvent, elapsed_time:float) -> GameEvent:
        ret: GameEvent = None
        if ev == GameEvent.INPUTEVENT_LEFT:
            self._try_move(state, dx=self._C_MOVE_LEFT_X_DELTA, dy=0)
        elif ev == GameEvent.INPUTEVENT_RIGHT:
            self._try_move(state, dx=self._C_MOVE_RIGHT_X_DELTA, dy=0)
        elif ev == GameEvent.INPUTEVENT_SOFT_DROP:
            self._try_move(state, dx=0, dy=self._C_MOVE_DROP_Y_DELTA)
        elif ev == GameEvent.INPUTEVENT_HARD_DROP:
            state.drop_delta = 0
            while self._try_move(state, dx=0, dy=self._C_MOVE_DROP_Y_DELTA):
                state.drop_delta += 1
                pass
        elif ev == GameEvent.INPUTEVENT_TICK:
            moved = self._try_move(state, dx=0, dy=self._C_MOVE_DROP_Y_DELTA)
            if not moved:
                self.update_last_lockdown_info(state)
                self.create_new_piece(state)
                return GameEvent.INPUTEVENT_NEW_ACTIVE_MINO_CREATED
        return ret

    """
    キー入力に従ってテトリミノを回転させる。
    """
    def rotate_piece(self, state: GameModel) -> None:
        rotated = state.active_piece.rotated(+1)
        if state.matrix.can_place(rotated, state.active_pos):
            state.active_piece = rotated
        else:
            # 回転できない場合は何もしない
            pass

    """
    キー入力に従ってテトリミノを移動させる。
    """
    def _try_move(self, state: GameModel, dx: int, dy: int) -> bool:
        x, y = state.active_pos
        new_pos = (x + dx, y + dy)
        if state.matrix.can_place(state.active_piece, new_pos):
            state.active_pos = new_pos
            return True
        return False

    def _lock_and_spawn(self, state: GameModel) -> None:
        state.matrix.lock(state.active_piece, state.active_pos, color_id=1)
        cleared = state.matrix.clear_lines()    # 暫定、LOCKした後で Line をクリアする処理は Matrix クラスに任せたい
        if cleared > 0:
            state.lines += cleared
            state.score += cleared * 100

    def update_last_lockdown_info(self, state: GameModel) -> None:
        state.last_lockdown_piece = state.active_piece
        state.last_lockdown_pos = state.active_pos
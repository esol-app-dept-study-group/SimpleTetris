from SimpleTetris.updater_base import UpdaterBase
from SimpleTetris.eventdef import GameEvent
from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus

class GameLogicMatrixUpdater(UpdaterBase):
    """Matrix に関する確定更新を担当する Updater。

    新規アクティブミノ生成イベントを「直前ミノの着地完了」とみなし、
    盤面固定・ライン削除・関連イベント発行を行う。
    """
    def __call__(self, state: GameModel, event: EventBus, elapsed_time:float) -> GameModel:
        # TetriminoUpdater が次ミノ生成を通知した tick で、直前ミノを盤面へ確定する。
        if event.has_event(GameEvent.INPUTEVENT_NEW_ACTIVE_MINO_CREATED):
            # 直前の固定対象（未設定時は現在値にフォールバック）。
            piece = getattr(state, "last_lockdown_piece", state.active_piece)
            pos = getattr(state, "last_lockdown_pos", state.active_pos)

            # ミノ種別に対応する色IDで盤面へ固定。
            color_id = state.matrix.color_id_for_kind(piece.kind)
            state.matrix.lock(piece, pos, color_id)

            # 1回の固定で発生したライン削除数を state に保持。
            cleared = state.matrix.clear_lines()
            state.last_lines_cleared = cleared
            if cleared > 0:
                # ライン削除の有無を次 tick で他 Updater が参照できるよう通知。
                event.emit(GameEvent.INPUTEVENT_LINE_CLEARED)

            # 固定完了イベントは毎回発行（スコア/レベル計算のトリガー）。
            event.emit(GameEvent.INPUTEVENT_TETRIMINO_LOCKDOWN)

        return state
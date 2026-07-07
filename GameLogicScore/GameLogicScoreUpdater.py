from SimpleTetris.updater_base import UpdaterBase
from SimpleTetris.eventdef import GameEvent
from SimpleTetris.GameModel import GameModel
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus

#<<ロジック>>
# <レベルとドロップによる特典の計算>
#  GameModelからstate.levelを取得し、対応するスコア倍率をローカル変数に保持
#  ハードのイベントが来たらDROP値を2倍、何もなければDROP値を1倍にする（ハード/ソフトを決めるのにタイムリミットがある前提）。ローカル変数に保持

#ラインクリアのイベントが来る
#LINE値を更新する
#CURRENT_SCOREをアップデートする

#レベルに応じたスコア倍率（仮置き。仕様書を確認し適切な値に変更予定）
LEVEL_TABLE = {
    1: 1,   #レベル1のときのスコア倍率
    2: 1.5, #レベル2のときのスコア倍率
    3: 2,   #レベル3のときのスコア倍率
    4: 2.5, #レベル4のときのスコア倍率
    5: 3,   #レベル5のときのスコア倍率
}

#揃え方によるスコア値(仮置き)
LINE_TABLE = {
    #0: 0,   #ラインを消さなかったときのスコア　(ライン消去イベントがラインが消えないときにも来る前提)
    1: 1,   #1段消しにより獲得するスコア
    2: 2,   #2段消しにより獲得するスコア
    3: 3,   #3段消しにより獲得するスコア
    4: 4,   #4段消しにより獲得するスコア
}

class GameLogicScoreUpdater(UpdaterBase):
    def __call__(self, state: GameModel, event: EventBus, elapsed_time: float) -> GameModel:
        # レベルを受け取る、レベル値を更新する
        award_for_currentlevel = LEVEL_TABLE[state.level]  # GameModelからレベルを取得し、対応するスコア倍率を適用する
        
        # ハードかソフトかの情報が入力される、DROP値を更新する 落ちたライン数によってスコアが変わる。要修正
        if event.has_event(GameEvent.INPUTEVENT_HARD_DROP):
            award_for_drop = 2
        else:
            award_for_drop = 1

        # ラインクリアイベントを受け取り、スコア加算
        if event.has_event(GameEvent.INPUTEVENT_LINE_CLEARED):#ロックダウンが更新されると発行（未実装）
            # イベントペイロードから消せたラインの数を取得
            cleared_lines = event.get_event_data(GameEvent.INPUTEVENT_LINE_CLEARED)
            # 計算されたスコアをCURRENT_SCOREに加算
            state.score += LINE_TABLE[cleared_lines] * award_for_currentlevel * award_for_drop

        return state

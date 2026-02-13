import pygame
from pygame.locals import *
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

    def get_event(self) -> list[GameEvent]:
        s = input("Command (a/d/w/s/space/q, Enter=tick): ").strip().lower()
        ret = []
        if s == "a":
            ret.append(GameEvent.INPUTEVENT_LEFT)
        if s == "d":
            ret.append(GameEvent.INPUTEVENT_RIGHT)
        if s == "w":
            ret.append(GameEvent.INPUTEVENT_ROTATE) 
        if s == "s":
            ret.append(GameEvent.INPUTEVENT_SOFT_DROP)
        if s == " " or s == "space":
            ret.append(GameEvent.INPUTEVENT_HARD_DROP)
        if s == "q":
            ret.append(GameEvent.INPUTEVENT_QUIT)
        if not ret:
            ret.append(GameEvent.INPUTEVENT_TICK)
        return ret

class PygameInputAdapter:
    def get_event(self) -> list[GameEvent]:
        ret = []
        # イベント処理
        for event in pygame.event.get():
            # 閉じるボタンが押されたら終了
            if event.type == QUIT: 
                ret.append( GameEvent.INPUTEVENT_QUIT )
            # キーイベント
            if event.type == KEYDOWN:
                # Escキーが押されたら終了
                if event.key == K_ESCAPE:
                    ret.append( GameEvent.INPUTEVENT_QUIT )
                # 矢印キーなら円の中心座標を矢印の方向に移動
                if event.key == K_LEFT:
                    ret.append( GameEvent.INPUTEVENT_LEFT )
                if event.key == K_RIGHT:
                    ret.append( GameEvent.INPUTEVENT_RIGHT )
                if event.key == K_UP:
                    ret.append( GameEvent.INPUTEVENT_ROTATE )
                if event.key == K_DOWN:
                    ret.append( GameEvent.INPUTEVENT_SOFT_DROP )   # 使わないけど、一応対応しておく
                if event.key == K_SPACE:
                    ret.append( GameEvent.INPUTEVENT_HARD_DROP )
        ret.append(GameEvent.INPUTEVENT_TICK)
        return ret
    
class InputAdapter:
    def __init__(self):
        self.core = PygameInputAdapter()
    def get_event(self) -> list[GameEvent]:
        return self.core.get_event()

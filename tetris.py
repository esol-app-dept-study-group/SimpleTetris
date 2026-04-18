# tetris_example.py
from __future__ import annotations
import os
import sys

# Allow running both as `python -m tetris.tetris` and `python tetris/tetris.py`
if __package__ is None or __package__ == "":
    # When executed as a script, sys.path[0] is the package dir (tetris/),
    # which makes Python find tetris.py as the top-level module and breaks
    # package imports. Remove that and add the parent instead.
    pkg_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(pkg_dir)
    if pkg_dir in sys.path:
        sys.path.remove(pkg_dir)
    sys.path.insert(0, parent_dir)
    __package__ = "SimpleTetris"
from SimpleTetris.AbstractModule.Platform import TkinterPlatform, ConsolePlatform, ConsolePygamePlatform, PygamePlatform
from SimpleTetris.GameModel import GameModel
from SimpleTetris.GameView import GameView
from SimpleTetris.GameUpdater import GameUpdater
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus

# ============================================================
# メインループ
# ============================================================
def run():
    #platform = TkinterPlatform()          # ここを差し替えるだけでバックエンドが切り替わる
    #platform = ConsolePlatform()           # ここを差し替えるだけでバックエンドが切り替わる
    #platform = ConsolePygamePlatform()      # ここを差し替えるだけでバックエンドが切り替わる
    platform = PygamePlatform()           # ここを差し替えるだけでバックエンドが切り替わる

    model = GameModel.initial()
    updater = GameUpdater()
    view = GameView(platform.graphics)   # gfx を DI
    eventbus = EventBus()

    def tick() -> bool:
        return run_gameloop_once(model, updater, view, platform.input, eventbus)

    platform.start_loop(tick, interval_ms=200)
    platform.quit()
    print("Bye!")

# 外部ゲームループから呼ばれるメイン処理
def run_gameloop_once(model, updater, view, input_adapter, eventbus):
    view(model)
    if model.is_GameOver():
        return True

    # 入力イベントの詰め替え
    for event in input_adapter.get_event():
        eventbus.emit(event)
    model = updater(model, eventbus)
    eventbus.end_tick()
    return False

if __name__ == "__main__":
    import sys; print(sys.executable)
    run()

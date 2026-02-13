# tetris_example.py
from __future__ import annotations
from enum import Enum, auto
from typing import List, Tuple, Dict, Optional
import random
import os
import sys
import time
import pygame
from pygame.locals import *

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
from SimpleTetris.AbstractModule.GraphicsAdapter import GraphicsAdapter
from SimpleTetris.AbstractModule.InputAdapter import InputAdapter
from SimpleTetris.GameModel import GameModel
from SimpleTetris.GameView import GameView
from SimpleTetris.GameUpdater import GameUpdater
from SimpleTetris.AbstractModule.common_tool.EventBus import EventBus

# ============================================================
# メインループ
# ============================================================
def run():
    # pygameの初期化
    pygame.init()                                   # Pygameの初期化
    screen = pygame.display.set_mode((1, 1), pygame.NOFRAME)
    pygame.display.set_caption("SimpleTetris")              # 画面上部に表示するタイトルを設定
    
    # ゲームロジック用のオブジェクト群を生成
    model = GameModel.initial()
    updater = GameUpdater()
    view = GameView()
    input_adapter = InputAdapter()
    eventbus = EventBus()

    while True:
        if run_gameloop_once(model, updater, view, input_adapter, eventbus):
            break

    pygame.quit()
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
    run()

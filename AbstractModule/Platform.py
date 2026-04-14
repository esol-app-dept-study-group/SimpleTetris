from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable
import time

import tkinter
import pygame
from pygame.locals import *

from SimpleTetris.AbstractModule.GraphicsAdapter import (
    GraphicsAdapter, ConsoleGraphicsAdapter, TkinterGraphicsAdapter, PygameGraphicsAdapter,
)
from SimpleTetris.AbstractModule.InputAdapter import (
    InputAdapter, ConsoleInputAdapter, PygameInputAdapter, TkinterInputAdapter,
)


class Platform(ABC):
    """グラフィックス・入力・イベントループを一体として管理する抽象基底クラス。
    バックエンド（Console / tkinter+pygame / 将来の pygame / Godot 等）ごとに
    このクラスを派生させて差し替える。
    """

    @property
    @abstractmethod
    def graphics(self) -> GraphicsAdapter: ...

    @property
    @abstractmethod
    def input(self) -> InputAdapter: ...

    @abstractmethod
    def start_loop(self, tick_func: Callable[[], bool], interval_ms: int = 50) -> None:
        """ゲームループを開始する。tick_func() が True を返したら終了する。"""
        ...

    @abstractmethod
    def quit(self) -> None:
        """バックエンド固有の終了処理"""
        ...


class ConsolePlatform(Platform):
    """コンソール出力 + コンソール入力"""

    def __init__(self):
        self._gfx = ConsoleGraphicsAdapter()
        self._inp = ConsoleInputAdapter()

    @property
    def graphics(self) -> GraphicsAdapter:
        return self._gfx

    @property
    def input(self) -> InputAdapter:
        return self._inp

    def start_loop(self, tick_func: Callable[[], bool], interval_ms: int = 50) -> None:
        # ConsoleInputAdapter は input() でブロックするため interval_ms は使わない
        while not tick_func():
            pass

    def quit(self) -> None:
        pass

class ConsolePygamePlatform(Platform):
    """Console 描画 + Pygame キー入力。
    """

    def __init__(self):
        # pygame は入力受付用（非表示の最小ウィンドウで初期化）
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.NOFRAME)

        # Adapter を生成して root を DI
        self._gfx = ConsoleGraphicsAdapter()
        self._inp = PygameInputAdapter()

    @property
    def graphics(self) -> GraphicsAdapter:
        return self._gfx

    @property
    def input(self) -> InputAdapter:
        return self._inp

    def start_loop(self, tick_func: Callable[[], bool], interval_ms: int = 50) -> None:
        interval_sec = interval_ms / 1000.0
        while True:
            start = time.perf_counter()
            if tick_func():
                break
            elapsed = time.perf_counter() - start
            remaining = interval_sec - elapsed
            if remaining > 0:
                time.sleep(remaining)

    def quit(self) -> None:
        pygame.quit()


class TkinterPlatform(Platform):
    """tkinter 描画 + tkinter キー入力。
    root / canvas は本クラスが所有し、外部には公開しない。

    ※ TkinterPygamePlatform（tkinter 描画 + Pygame キー入力）は実現不可。
      tkinter ウィンドウがフォーカスを持つため pygame がキーイベントを受け取れない。
    """

    def __init__(self):
        # tkinter メインウィンドウ
        self._root = tkinter.Tk()
        self._root.title("SimpleTetris")
        self._root.geometry("400x600")

        # Adapter を生成して root を DI
        self._gfx = TkinterGraphicsAdapter(self._root)
        self._inp = TkinterInputAdapter(self._root)  # tkinter がフォーカスを持つためtkinter側でキーを受け取る

    @property
    def graphics(self) -> GraphicsAdapter:
        return self._gfx

    @property
    def input(self) -> InputAdapter:
        return self._inp

    def start_loop(self, tick_func: Callable[[], bool], interval_ms: int = 50) -> None:
        def _tick():
            if not tick_func():
                self._root.after(interval_ms, _tick)
            else:
                self._root.destroy()

        self._root.after(0, _tick)
        self._root.mainloop()

    def quit(self) -> None:
        pass

class PygamePlatform(Platform):
    """Pygame 描画 + Pygame キー入力。
    """

    def __init__(self):
        # pygame ウインドウ
        pygame.init()
        screen = pygame.display.set_mode((400, 600))
        pygame.display.set_caption("SimpleTetris")
        pygame.display.flip()

        # Adapter を生成して root を DI
        self._gfx = PygameGraphicsAdapter(screen)
        self._inp = PygameInputAdapter()

    @property
    def graphics(self) -> GraphicsAdapter:
        return self._gfx

    @property
    def input(self) -> InputAdapter:
        return self._inp

    def start_loop(self, tick_func: Callable[[], bool], interval_ms: int = 50) -> None:
        interval_sec = interval_ms / 1000.0
        while True:
            start = time.perf_counter()
            if tick_func():
                break
            elapsed = time.perf_counter() - start
            remaining = interval_sec - elapsed
            if remaining > 0:
                time.sleep(remaining)

    def quit(self) -> None:
        pygame.quit()

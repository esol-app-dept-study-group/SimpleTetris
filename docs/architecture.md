# SimpleTetris アーキテクチャ設計ドキュメント

## 目次

1. [プロジェクト概要](#1-プロジェクト概要)
2. [ディレクトリ構成](#2-ディレクトリ構成)
3. [アーキテクチャ概要](#3-アーキテクチャ概要)
4. [クラス図](#4-クラス図)
   - [ドメイン層](#41-ドメイン層)
   - [モデル層](#42-モデル層)
   - [Updater 層](#43-updater-層)
   - [View 層](#44-view-層)
   - [プラットフォーム抽象層](#45-プラットフォーム抽象層)
5. [シーケンス図](#5-シーケンス図)
   - [起動シーケンス](#51-起動シーケンス)
   - [1 tick の処理フロー](#52-1-tick-の処理フロー)
6. [イベント発行・購読マップ](#6-イベント発行購読マップ)
   - [GameEvent 一覧](#61-gameevent-一覧)
   - [発行者と購読者の対応表](#62-発行者と購読者の対応表)
   - [イベントフロー図](#63-イベントフロー図)

---

## 1. プロジェクト概要

SimpleTetris は Python で実装されたテトリスゲームです。  
MVC に近いレイヤード構成と、**EventBus** を介したイベント駆動設計を採用しています。

バックエンド（描画・入力）はアダプタパターンで抽象化されており、  
`tetris.py` の Platform を 1 行差し替えるだけで以下の 4 つのバックエンドを切り替えられます。

| Platform クラス       | 描画        | 入力       |
|-----------------------|-------------|------------|
| `ConsolePlatform`     | コンソール  | コンソール |
| `ConsolePygamePlatform` | コンソール | Pygame     |
| `TkinterPlatform`     | tkinter     | tkinter    |
| `PygamePlatform`      | Pygame      | Pygame     |

---

## 2. ディレクトリ構成

```
SimpleTetris/
├── tetris.py                        # エントリポイント・ゲームループ
├── domain.py                        # ドメインオブジェクト（Matrix, Tetromino）
├── GameModel.py                     # ゲームステートモデル
├── GameUpdater.py                   # Updater コーディネータ
├── GameView.py                      # View コーディネータ
├── updater_base.py                  # Updater 抽象基底クラス
├── view_base.py                     # View 抽象基底クラス
├── eventdef.py                      # イベント定義（GameEvent enum）
├── TetriminoDef.py                  # テトリミノ種別定義（TetriminoType enum）
│
├── AbstractModule/                  # プラットフォーム抽象層
│   ├── GraphicsAdapter.py           # 描画アダプタ基底 + 具体実装
│   ├── InputAdapter.py              # 入力アダプタ基底 + 具体実装
│   ├── Platform.py                  # Platform 基底 + 具体実装
│   └── common_tool/
│       └── EventBus.py              # EventBus（tick 単位イベントキュー）
│
├── GameLogicLevel/
│   └── GameLogicLevelUpdater.py     # レベル管理 Updater
│
├── GameLogicNextMino/
│   ├── GameLogicNextMinoUpdater.py  # ネクストミノキュー管理 Updater
│   └── NextMinoPermutation.py       # ランダム順列生成ユーティリティ
│
├── GameLogicTetrimino/              # ※実装途中
│   ├── GameLogicTetriminoUpdater.py # テトリミノ操作 Updater（WIP）
│   └── GameLogicTetriminoModel.py   # テトリミノモデル（WIP）
│
├── sample/                          # 参照実装（動作する暫定実装）
│   ├── SampleUpdater.py             # 参照 Updater 実装
│   └── SampleView.py                # 参照 View 実装
│
└── docs/                            # ドキュメント
```

---

## 3. アーキテクチャ概要

```
┌──────────────────────────────────────────────────────────────────┐
│                         tetris.py                                │
│  Platform.start_loop() が run_gameloop_once() を繰り返し呼び出す │
└────────────────────┬─────────────────────────────────────────────┘
                     │
         ┌───────────▼──────────────────────────────────────┐
         │             run_gameloop_once()                   │
         │                                                   │
         │  1. GameView(model)          ← 描画               │
         │  2. InputAdapter.get_event() ← 入力取得           │
         │  3. eventbus.emit(event)     ← EventBus に積む    │
         │  4. GameUpdater(model, bus)  ← 状態更新           │
         │  5. eventbus.end_tick()      ← tick 終了処理      │
         └───────────────────────────────────────────────────┘

  ┌─────────────┐   ┌──────────────┐   ┌───────────────────────┐
  │  GameModel  │   │  GameUpdater │   │       GameView        │
  │  (状態保持) │◄──│ (状態変換)   │   │  (状態→描画への変換)  │
  └─────────────┘   └──────┬───────┘   └───────────────────────┘
                            │
              ┌─────────────┼───────────────────┐
              ▼             ▼                   ▼
     SampleUpdater  GameLogicLevelUpdater  GameLogicNextMinoUpdater
                                           GameLogicTetriminoUpdater
```

**設計上のポイント:**

- `GameModel` はイミュータブルではなく、Updater が直接フィールドを更新するスタイル。
- `EventBus` は 1 tick 分のイベントを安全に受け渡すキュー。`emit()` は次 tick 用、`poll()` は現在 tick 用のキューを読む。
- `InputAdapter` は外部入力を `GameEvent` に変換するだけの薄いアダプタ。  
  実際の `EventBus.emit()` は `tetris.py` が担う。

---

## 4. クラス図

### 4.1 ドメイン層

```mermaid
classDiagram
    class Tetromino {
        +str kind
        +int rotation
        +blocks() List~Point~
        +rotated(delta) Tetromino
    }

    class Matrix {
        +int width
        +int height
        +List cells
        +in_bounds(x, y) bool
        +is_empty(x, y) bool
        +can_place(piece, pos) bool
        +lock(piece, pos, color_id) None
        +clear_lines() int
    }

    class TetriminoType {
        I
        O
        T
        S
        Z
        J
        L
    }
    Tetromino --> TetriminoType : kind
    Matrix --> Tetromino : can_place and lock
```

### 4.2 モデル層

```mermaid
classDiagram
    class GameModel {
        +Matrix matrix
        +Tetromino active_piece
        +Point active_pos
        +List~str~ next_queue
        +int score
        +int lines
        +int level
        +int goal
        +bool game_over
        +FALL_SPEED_MS Dict
        +is_GameOver() bool
        +get_fall_speed_ms() int
        +initial(width, height)$ GameModel
    }

    GameModel --> Matrix
    GameModel --> Tetromino
```

### 4.3 Updater 層

```mermaid
classDiagram
    class UpdaterBase {
        -last_called float
        +_compute_elapsed_ms() float
        +__call__(state, cmd, elapsed_time) GameModel*
    }

    class GameUpdater {
        +subUpdaterList List
        +__call__(state, event) GameModel
    }

    class SampleUpdater {
        +__call__(state, event, elapsed_time) GameModel
        -_try_move(state, dx, dy) bool
        -_try_rotate(state) None
        -_hard_drop(state) None
        -_lock_and_spawn(state) None
        -_next_kind(state) str
    }

    class GameLogicLevelUpdater {
        +__call__(state, event, elapsed_time) GameModel
    }

    class GameLogicNextMinoUpdater {
        +__call__(state, event, elapsed_time) GameModel
        +refill_mino(state) None
    }

    class GameLogicTetriminoUpdater {
        +__call__(state, event, elapsed_time) GameModel
        +create_new_piece(state) GameModel
        +move_piece(state, ev) None
        +rotate_piece(state) None
    }

    UpdaterBase <|-- SampleUpdater
    UpdaterBase <|-- GameLogicLevelUpdater
    UpdaterBase <|-- GameLogicNextMinoUpdater
    UpdaterBase <|-- GameLogicTetriminoUpdater

    GameUpdater o-- SampleUpdater
    GameUpdater o-- GameLogicLevelUpdater
    GameUpdater o-- GameLogicNextMinoUpdater
    GameUpdater o-- GameLogicTetriminoUpdater
```

### 4.4 View 層

```mermaid
classDiagram
    class ViewBase {
        +__call__(state) None*
    }

    class GameView {
        +subViewList List
        +__call__(state) GameModel
    }

    class SampleView {
        +gfx GraphicsAdapter
        +__call__(state) None
    }

    ViewBase <|-- SampleView
    GameView o-- SampleView
    SampleView --> GraphicsAdapter
```

### 4.5 プラットフォーム抽象層

```mermaid
classDiagram
    class Platform {
        +graphics GraphicsAdapter
        +input InputAdapter
        +start_loop(tick_func, interval_ms) None
        +quit() None
    }

    class ConsolePlatform {
        -_gfx ConsoleGraphicsAdapter
        -_inp ConsoleInputAdapter
    }

    class ConsolePygamePlatform {
        -_gfx ConsoleGraphicsAdapter
        -_inp PygameInputAdapter
    }

    class TkinterPlatform {
        -_root Tk
        -_gfx TkinterGraphicsAdapter
        -_inp TkinterInputAdapter
    }

    class PygamePlatform {
        -_gfx PygameGraphicsAdapter
        -_inp PygameInputAdapter
    }

    class GraphicsAdapter {
        +begin_frame() None
        +draw_matrix(vm) None
        +draw_active_piece(vm) None
        +draw_score(vm) None
        +draw_next(vm) None
        +end_frame() None
        +render(vm) None
    }

    class ConsoleGraphicsAdapter
    class TkinterGraphicsAdapter
    class PygameGraphicsAdapter

    class InputAdapter {
        +get_event() List~GameEvent~
    }

    class ConsoleInputAdapter
    class PygameInputAdapter
    class TkinterInputAdapter

    class EventBus {
        -_current_tick Deque
        -_next_tick Deque
        +emit(event) None
        +poll() Iterable~GameEvent~
        +end_tick() None
        +clear_all() None
    }

    Platform <|-- ConsolePlatform
    Platform <|-- ConsolePygamePlatform
    Platform <|-- TkinterPlatform
    Platform <|-- PygamePlatform

    GraphicsAdapter <|-- ConsoleGraphicsAdapter
    GraphicsAdapter <|-- TkinterGraphicsAdapter
    GraphicsAdapter <|-- PygameGraphicsAdapter

    InputAdapter <|-- ConsoleInputAdapter
    InputAdapter <|-- PygameInputAdapter
    InputAdapter <|-- TkinterInputAdapter

    ConsolePlatform --> ConsoleGraphicsAdapter
    ConsolePlatform --> ConsoleInputAdapter
    ConsolePygamePlatform --> ConsoleGraphicsAdapter
    ConsolePygamePlatform --> PygameInputAdapter
    TkinterPlatform --> TkinterGraphicsAdapter
    TkinterPlatform --> TkinterInputAdapter
    PygamePlatform --> PygameGraphicsAdapter
    PygamePlatform --> PygameInputAdapter
```

---

## 5. シーケンス図

### 5.1 起動シーケンス

```mermaid
sequenceDiagram
    actor User
    participant tetris as tetris.py
    participant Platform
    participant GameModel
    participant GameUpdater
    participant GameView
    participant EventBus

    User->>tetris: python tetris.py
    tetris->>Platform: PygamePlatform()（またはほか）
    Platform-->>tetris: platform
    tetris->>GameModel: GameModel.initial()
    GameModel-->>tetris: model
    tetris->>GameUpdater: GameUpdater()
    GameUpdater-->>tetris: updater
    tetris->>GameView: GameView(platform.graphics)
    GameView-->>tetris: view
    tetris->>EventBus: EventBus()
    EventBus-->>tetris: eventbus
    tetris->>Platform: start_loop(tick, interval_ms=200)
    loop ゲームループ
        Platform->>tetris: tick()
        tetris->>tetris: run_gameloop_once(...)
    end
    tetris->>Platform: quit()
```

### 5.2 1 tick の処理フロー

```mermaid
sequenceDiagram
    participant Tick as run_gameloop_once
    participant View as GameView
    participant Input as InputAdapter
    participant Bus as EventBus
    participant Updater as GameUpdater
    participant Sub as SubUpdaters

    Tick->>View: view(model)
    View->>View: SampleView.__call__(model)
    View->>View: gfx.render(vm) → 描画

    Tick->>Input: input_adapter.get_event()
    Input-->>Tick: GameEvent list

    loop 各 GameEvent
        Tick->>Bus: eventbus.emit(event)
        Note over Bus: _next_tick に積む
    end

    Tick->>Updater: updater(model, eventbus)
    loop 各 SubUpdater
        Updater->>Sub: sub(state, eventbus, elapsed_ms)
        Sub->>Bus: event.poll()
        Bus-->>Sub: _current_tick のイベント列
        Sub->>Sub: イベントに応じて model を更新
        Sub-->>Updater: updated state
    end
    Updater-->>Tick: updated model

    Tick->>Bus: eventbus.end_tick()
    Note over Bus: _next_tick → _current_tick にスワップ
```

---

## 6. イベント発行・購読マップ

### 6.1 GameEvent 一覧

`eventdef.py` で定義されている `GameEvent` の全イベントとその用途：

| イベント名 | 説明 |
|-----------|------|
| `INPUTEVENT_INITIALIZED` | ゲーム開始時に一度だけ送られる（`tetris.py` `run()` が発行） |
| `INPUTEVENT_TICK` | 定期タイマー（毎 tick 必ず発行） |
| `INPUTEVENT_LEFT` | 左移動入力 |
| `INPUTEVENT_RIGHT` | 右移動入力 |
| `INPUTEVENT_ROTATE` | 回転入力 |
| `INPUTEVENT_SOFT_DROP` | ソフトドロップ入力 |
| `INPUTEVENT_HARD_DROP` | ハードドロップ入力 |
| `INPUTEVENT_QUIT` | 終了入力 |
| `INPUTEVENT_LINE_CLEARED` | ラインクリア発生時（※現在未発行） |
| `INPUTEVENT_TETRIMINO_LOCKDOWN` | テトリミノのロックダウン時（※現在未発行） |

> **※注意:** `INPUTEVENT_LINE_CLEARED`, `INPUTEVENT_TETRIMINO_LOCKDOWN` は  
> 購読側（`GameLogicTetriminoUpdater`）は対応済みだが、現在の実装では発行されていない。  
> `INPUTEVENT_INITIALIZED` は `tetris.py` の `run()` でループ開始前に一度だけ発行される。

### 6.2 発行者と購読者の対応表

| GameEvent | 発行者 | 購読者（反応するクラス） | 何をするか？  |
|-----------|--------|--------------------------|------------|
| `INPUTEVENT_INITIALIZED` | `tetris.py` `run()`（ループ開始前に一度だけ） | `GameLogicTetriminoUpdater` | 新しい ActiveTetrimino を作成してゲームを開始する |
| `INPUTEVENT_TICK` | `ConsoleInputAdapter` / `PygameInputAdapter` / `TkinterInputAdapter`（毎 tick 自動発行） | `SampleUpdater` / `GameLogicLevelUpdater` / `GameLogicTetriminoUpdater` | ActiveTetrimino を１つ落下させる |
| `INPUTEVENT_LEFT` | `ConsoleInputAdapter` / `PygameInputAdapter` / `TkinterInputAdapter` | `SampleUpdater` / `GameLogicTetriminoUpdater` | ActiveTetrimino を１つ左に移動させる |
| `INPUTEVENT_RIGHT` | `ConsoleInputAdapter` / `PygameInputAdapter` / `TkinterInputAdapter` | `SampleUpdater` / `GameLogicTetriminoUpdater` | ActiveTetrimino を１つ右に移動させる |
| `INPUTEVENT_ROTATE` | `ConsoleInputAdapter` / `PygameInputAdapter` / `TkinterInputAdapter` | `SampleUpdater` / `GameLogicTetriminoUpdater` | ActiveTetrimino を回転させる |
| `INPUTEVENT_SOFT_DROP` | `ConsoleInputAdapter` / `PygameInputAdapter` / `TkinterInputAdapter` | `SampleUpdater` / `GameLogicTetriminoUpdater` | ActiveTetrimino を１つソフトドロップさせる |
| `INPUTEVENT_HARD_DROP` | `ConsoleInputAdapter` / `PygameInputAdapter` / `TkinterInputAdapter` | `SampleUpdater` / `GameLogicTetriminoUpdater` | ActiveTetrimino をハードドロップさせる |
| `INPUTEVENT_QUIT` | （未実装・`GameLogicMatrixUpdater`付近から発行予定）  / `PygameInputAdapter` / `TkinterInputAdapter` | `SampleUpdater` / `GameLogicTetriminoUpdater` | ゲームを終了させる |
| `INPUTEVENT_LINE_CLEARED` | （未実装・`GameLogicTetriminoUpdater` 付近から発行予定） | `GameLogicScoreUpdater` / `GameLogicLevelUpdater` |  スコア計算し、レベル上昇処理を行う |
| `INPUTEVENT_TETRIMINO_LOCKDOWN` | （未実装・`GameLogicTetriminoUpdater._lock_and_spawn()` 付近から発行予定） | `GameLogicTetriminoUpdater` | ロックダウンを実施し |ライン消去し、新しい ActiveTetriminoを作成する |

> **発行の仕組み:**  
> InputAdapter は `get_event()` で `GameEvent` のリストを返すだけです。  
> `tetris.py` の `run_gameloop_once()` がそのリストを受け取り、  
> `eventbus.emit(event)` を呼んで EventBus に積みます。

### 6.3 イベントフロー図

```mermaid
flowchart TD
    subgraph InputAdapter
        CON[ConsoleInputAdapter]
        PYG[PygameInputAdapter]
        TKI[TkinterInputAdapter]
    end

    subgraph tetris_py
        EMIT[eventbus.emit]
        INIT_EMIT[tetris run: INITIALIZED 発行<br/>起動時一度だけ]
    end

    subgraph EventBus
        QUEUE[_next_tick キュー]
        SWAP[end_tick: swap]
        CURR[_current_tick キュー]
    end

    subgraph SubUpdaters
        SAMP[SampleUpdater<br/>poll: QUIT/LEFT/RIGHT/ROTATE<br/>SOFT_DROP/HARD_DROP/TICK]
        LEVL[GameLogicLevelUpdater<br/>poll: TICK]
        NEXT[GameLogicNextMinoUpdater<br/>※イベント不使用・無条件補充]
        TETR[GameLogicTetriminoUpdater<br/>poll: INITIALIZED/LOCKDOWN<br/>LINE_CLEARED/LEFT/RIGHT<br/>ROTATE/SOFT_DROP/HARD_DROP<br/>TICK/QUIT]
    end

    CON -->|get_event| EMIT
    PYG -->|get_event| EMIT
    TKI -->|get_event| EMIT
    EMIT --> QUEUE
    INIT_EMIT --> QUEUE
    QUEUE --> SWAP
    SWAP --> CURR
    CURR -->|poll| SAMP
    CURR -->|poll| LEVL
    CURR -->|poll| NEXT
    CURR -->|poll| TETR

    style NEXT fill:#f9f,stroke:#999,color:#333
```

```mermaid
flowchart LR
    subgraph GameEvent
        INIT[INITIALIZED]
        TICK[TICK]
        LEFT[LEFT]
        RIGHT[RIGHT]
        ROTATE[ROTATE]
        SDROP[SOFT_DROP]
        HDROP[HARD_DROP]
        QUIT[QUIT]
        LCLR[LINE_CLEARED（未発行）]
        LOCK[TETRIMINO_LOCKDOWN]
    end

    subgraph 発効する人
        PA[各 InputAdapter<br/>毎 tick]
        PB[各 InputAdapter<br/>キー入力時]
        PTETRIS[tetris.py run<br/>起動時一度だけ]
        PNOTIMPL[未実装]
        PLOCKDOWN[GameLogicTetriminoUpdater<br/>テトリミノロックダウン]
    end

    subgraph 受信する人
        SB[GameLogicLevelUpdater]
        SC[GameLogicTetriminoUpdater]
        SD[GameLogicMatrixUpdater]
        SE[GameLogicScoreUpdater<br />（未実装）]
    end

    PA -->|TICK| TICK
    PLOCKDOWN -->|LOCKDOWN| LOCK
    PB -->|操作系| LEFT & RIGHT & ROTATE & SDROP & HDROP & QUIT
    PTETRIS -->|起動時| INIT
    PNOTIMPL -->|将来| LCLR

    TICK --> SB & SC
    LEFT & RIGHT & ROTATE & SDROP & HDROP --> SC
    QUIT --> SC
    INIT & LOCK --> SC
    LCLR --> SD & SB
    LOCK --> SD & SE

    style INIT fill:#dfd,stroke:#090
    style LCLR fill:#fdd,stroke:#c00
    style PNOTIMPL fill:#fdd,stroke:#c00
    style PTETRIS fill:#dfd,stroke:#090
    style SE fill:#fdd,stroke:#c00
```

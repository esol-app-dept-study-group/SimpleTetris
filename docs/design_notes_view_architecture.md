# SimpleTetris View 設計メモ

日付: 2026年3月23日

---

## 背景・前提

SimpleTetris は MVU パターンで実装されており、以下の5モジュールへの分割を進めている。

- Score
- Level
- NextMino
- Tetrimino
- Matrix

各モジュールは Model / View / Updater の責務を持つ。  
Model / Updater については責務分けができているが、**View の設計について課題がある。**

### 現状の View 実装

- `SampleView` の中で `ViewModel` を組み立て、`GraphicsAdapter` 経由で描画する
- `ViewModel.cells` は `List[List[int]]` のセル配列で、固定ブロックと操作中ミノを混在させている
- `self.gfx.render(vm)` を1箇所でコールしている

---

## 課題

### 課題1: 操作中テトリミノのピクセル精度描画

`cells: List[List[int]]` にセルIDとして混ぜ込む限り、操作中テトリミノのピクセル単位のなめらかな描画ができない。

今後は **`GameLogicTetriminoView` が単独で操作中テトリミノの描画を担う** 方向が望ましい。  
その場合、`vm.cells` からは操作中ミノを除外し、Matrix は固定ブロックだけを表現する。

### 課題2: 複数 SubView の描画タイミング統一

SubView を分割すると、各 SubView が個別に `gfx.render()` を叩く可能性がある。  
エンジンによって「画面への commit」タイミングが異なるため（pygame の `display.update()`、Godot の `queue_redraw()` 等）、描画タイミングを一致させる仕組みが必要。

---

## 推奨設計: `begin_frame` / `end_frame` パターン

`GraphicsAdapter` に `begin_frame()` / `end_frame()` を追加し、`GameView` が全体のフレームライフサイクルを管理する。

```
GameView.__call__(state)
  │
  ├─ gfx.begin_frame()              ← バックバッファクリア、描画準備
  │
  ├─ MatrixView(state)               → gfx.draw_matrix(matrix_vm)
  ├─ GameLogicTetriminoView(state)   → gfx.draw_active_piece(piece_vm)
  │                                     ※ piece_vm はピクセル座標・速度を持てる
  ├─ ScoreView(state)                → gfx.draw_score(score_vm)
  ├─ NextMinoView(state)             → gfx.draw_next(next_vm)
  │
  └─ gfx.end_frame()               ← pygame: display.flip(), Godot: commit, Console: flush
```

各 SubView は「自分の担当データを `gfx.draw_xxx()` に渡す」責務のみ。  
「いつ画面に反映するか」は `GameView` が `end_frame()` で一元管理する。

### エンジン別 `end_frame()` 実装イメージ

| エンジン | `begin_frame()` | `end_frame()` |
|----------|----------------|---------------|
| Console | 画面クリア (`cls`) | バッファを一括 print |
| pygame | バックバッファクリア | `pygame.display.flip()` |
| Godot | - | ノードの座標・速度を設定 → `queue_redraw()` |

---

## `ActivePieceViewModel` の導入

操作中テトリミノ専用の ViewModel を別途定義し、セル座標系とは独立したピクセル座標・速度を持たせる。

```python
@dataclass
class ActivePieceViewModel:
    kind: str           # テトリミノ種別
    blocks: List[...]   # ブロック形状
    pixel_x: float      # ピクセル座標 X
    pixel_y: float      # ピクセル座標 Y
    velocity_y: float   # 落下速度 (pixel/sec)
```

`gfx.draw_active_piece(piece_vm)` に渡すことで、エンジン側がなめらかなアニメーションを実現できる。

---

## 既存の `render(vm)` との互換

`ConsoleGraphicsAdapter` のような「一発描画」エンジンでは、`render(vm)` を `begin_frame` + 全描画 + `end_frame` を内包した便宜メソッドとして残すことも可能。  
将来エンジンを追加する際に `begin_frame` / `draw_xxx` / `end_frame` を実装する形に段階的移行できる。

---

## まとめ

| 課題 | 解決策 |
|------|--------|
| SubView 分割後の render タイミング統一 | `GameView` が `begin_frame` / `end_frame` を管理 |
| エンジン固有の commit 処理の抽象化 | `end_frame()` を `GraphicsAdapter` の抽象メソッドに |
| ピクセル精度 vs セル座標の共存 | `draw_active_piece(piece_vm)` を別メソッドとして分離 |
| Z順序・描画順の制御 | `GameView` における `subViewList` の呼び出し順で管理 |

現在の `GameView.subViewList` 構造を活かしつつ、最小限の変更で実現可能。

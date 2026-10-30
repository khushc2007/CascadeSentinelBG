# Attract mode — the third screen

`attract.html` is a 90-second cinematic loop for the presentation laptop. It is one self-contained file (about 175 KB): it needs no internet and no server, so you can just double-click it. It is built from the project's real IEEE-118 data: the worst triple {6, 67, 140}, a DC cascade over 7 rounds with 97 trips, 31 buses dark and 22.8 % of demand unserved.

## Run
Open `attract.html` in Chrome or Edge, then press **F** for fullscreen.

| Key | Action |
|---|---|
| F | fullscreen |
| H | hide or show the HUD |
| Space / P | pause |
| ← / → | seek 5 s |
| 1–7 | jump to a scene |
| 0 | restart |
| D | debug overlay (fps, quality level, data check) |
| M | ambient sound (off by default) |

URL options: `?t=SECONDS`, `?still=1`, `?q=high|mid|low`, `?speed=N` and `?hud=0`.

## Scenes
| Time | Scene | What it shows |
|---|---|---|
| 0–6 s | Boot | Boot log |
| 6–20 s | Grid alive | The network appears |
| 20–28 s | The strike | Lines 6, 67 and 140 are taken out |
| 28–45 s | The cascade | 7 real rounds |
| 45–52 s | The number | 22.8 % of demand unserved |
| 52–64 s | The haystack | 1,055,240 candidates |
| 64–78 s | The quantum race | Grover (exact emulation), then the realistic cost estimate: ≈ 33,000× slower |
| 78–90 s | Restore and title | Lights come back, then the title card |

## Rebuild after data changes
```
python attract/build.py blacksky/site attract/attract.src.html attract/attract.html
```
The build asserts the derived numbers (97 / 7 / 31 / 22.8 % / branch 110 at 612 %). The page re-checks them on load: see the D overlay or the browser console.

## Engineering
- Raw WebGL2 with no libraries.
- HDR rendering, 6-level bloom, ACES tone mapping and screen-space shockwaves.
- Adaptive quality: render scale, particle count and galaxy point count step down when frames run long.
- Recovers from WebGL context loss, pauses when the tab is hidden, and keeps the screen awake.
- Calmer variant for reduced-motion users.

The animation's labels follow the project's evidence classes: SIM, EMU and EST. Its footer states that the network is a benchmark with synthetic ratings, that no quantum hardware was run, and that no quantum advantage is claimed.

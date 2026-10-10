# Garba Night — Auto-Mix

A structure-aware garba/dandiya set rendered with the open-source **automix** engine
(beat/downbeat/phrase grid + bass-swap, research-grounded MIR techniques), then
tuned to **A = 435 Hz**.

## What this is

Nine garba tracks are chained into one continuous, gapless, beat-matched set:

| # | Track | Role |
|---|---|---|
| 1 | Nagada Sang Dhol | devotional opener |
| 2 | Sanedo | warm-up |
| 3 | Gori Radha Ne Kalo Kaan | traditional lift |
| 4 | Khalasi | build (kinaare verse) |
| 5 | Udi Udi Jaye | rise |
| 6 | Chogada | peak |
| 7 | Kamariya | peak |
| 8 | Odhani | sustain |
| 9 | 56 Ni Chhati | close |

Each consecutive pair is tempo-locked, phrase-locked on an 8-bar grid, loudness-matched,
and bass-swapped on a downbeat. Transition types are chosen by the engine
(double_drop / relaxed / rolling).

## Output

- `garba_night_435hz.mp3` — 20:00, 320 kbps, tuned to A = 435 Hz (about 20 cents below A = 440).

## How it was rendered

1. Engine: `build_continuous_set()` from the open-source `automix` research prototype
   (saksham-45/automix) — librosa beat/phrase analysis, equal-power crossfade, 3-band
   bass swap.
2. Rendered at 22.05 kHz (memory-constrained CPU box); the engine streams the timeline
   to disk via `on_part`.
3. Tuning to 435 Hz applied to the finished mix, exactly, via:
   `asetrate=SR*(435/440), aresample=44100, atempo=(440/435)` — pitch down, tempo unchanged.
   Verified against a 440 Hz reference tone through the identical chain (lands at 435.0 Hz).
4. Trimmed to 20:00 with a fade-out, loudness-normalised, limited.

## Notes

- 435 Hz is about 20 cents below standard pitch. Some instruments/ensembles tune here
  historically; it is not the modern default (A = 440).
- Rendering at 22.05 kHz band-limits the top end (11 kHz). On a machine with more RAM
  the same engine renders at 44.1 kHz.
- Source tracks are local files supplied by the user; none are redistributed here.

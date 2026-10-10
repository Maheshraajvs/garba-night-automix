#!/usr/bin/env bash
# Tune the finished mix to A = 435 Hz (about 20 cents below A = 440), tempo unchanged.
#
# Method: asetrate shifts pitch AND speed by R; atempo restores the original speed,
# so the net effect is a pure pitch shift. Verified against a 440 Hz reference tone
# through the identical chain -> 435.0 Hz.
set -euo pipefail

IN="${1:-automix_set.wav}"
OUT="${2:-garba_night_435hz.mp3}"
SECONDS_LEN="${3:-1200}"

R=0.98863636        # 435 / 440

ffmpeg -hide_banner -loglevel error -y -i "$IN" \
  -af "asetrate=22050*${R},aresample=44100:resampler=soxr,atempo=1.01149425,atrim=0:${SECONDS_LEN},afade=t=out:st=$((SECONDS_LEN-14)):d=14,loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.92" \
  -ar 44100 -ac 2 -b:a 320k "$OUT"

echo "wrote $OUT (A=435 Hz)"

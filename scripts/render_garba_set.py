#!/usr/bin/env python3
"""Render the garba night set with the open-source automix engine.

Uses build_continuous_set() from the automix research prototype (saksham-45/automix):
beat/downbeat/phrase grid analysis, equal-power crossfade, 3-band bass swap.
Streams the timeline straight to disk via on_part() so a 20-minute set never has to
sit in RAM all at once.

Set AUTOMIX_DIR to the local checkout of the automix engine.
"""
import os, sys, time
AUTOMIX_DIR = os.environ.get('AUTOMIX_DIR', os.path.expanduser('~/automix'))
sys.path.insert(0, AUTOMIX_DIR)

import numpy as np, librosa, soundfile as sf
from src.club_mixer import build_continuous_set

SR = 22050          # 22.05 kHz keeps memory low on a small CPU box
BLEND_BARS = 4      # transition length in bars
SONGS_DIR = os.environ.get('SONGS_DIR', 'garba')

# (file, start_s, length_s) in energy-arc order: devotional opener -> peak -> close
plan = [
    ('08_nagada_sang_dhol.mp3',   0.0, 269.0),
    ('05_sanedo.mp3',             0.0, 133.0),
    ('02_gori_radha.mp3',         0.0, 176.0),
    ('03_khalasi.mp3',            0.0, 262.0),
    ('06_udi_udi.mp3',            0.0, 149.0),
    ('09_chogada.mp3',            0.0, 152.0),
    ('07_kamariya.mp3',           0.0, 185.0),
    ('01_odhani.mp3',             0.0, 139.0),
    ('04_chhati56.mp3',           0.0, 215.0),
]

def loader(path, start, length):
    def f():
        y, _ = librosa.load(path, sr=SR, mono=False, offset=start, duration=length)
        return (y.T if y.ndim == 2 else y).astype(np.float32)
    return f

tracks = [loader(os.path.join(SONGS_DIR, f), s, l) for f, s, l in plan]

out = sf.SoundFile('automix_set.wav', 'w', samplerate=SR, channels=2, subtype='PCM_16')
def on_part(part, marker=None):
    if part is not None and len(part):
        out.write(part)

t0 = time.time()
_, markers = build_continuous_set(tracks, sr=SR, blend_bars=BLEND_BARS, phrase_bars=8,
                                  progress=lambda i, n: print(f'  transition {i}/{n-1}', flush=True),
                                  on_part=on_part)
out.close()
print(f"rendered {sf.info('automix_set.wav').duration:.1f}s in {time.time()-t0:.0f}s")
for m in markers:
    print(' ', m)
print('wrote automix_set.wav')

#!/usr/bin/env python3
"""Generates an original, copyright-free music bed (assets/bed.wav): warm A-minor pad, soft bass,
light kick/hat and a gentle arpeggio at 96 BPM, 20 s, loopable. usage: python3 voice/make_music.py"""
import subprocess, numpy as np, soundfile as sf
from pathlib import Path
SR, BPM = 44100, 96
beat = 60 / BPM; bar = 4 * beat
CHORDS = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]] * 2   # Am F C G, twice
N = int(SR * bar * len(CHORDS)); t = np.arange(N) / SR; out = np.zeros(N)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def env(n, a, r):
    e = np.ones(n); ai, ri = int(a * SR), int(r * SR)
    e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.linspace(1, 0, ri); return e
def tone(f, n, harm=(1, .35, .15, .07), det=0.0):
    x = np.arange(n) / SR; return sum(a * np.sin(2 * np.pi * f * (k + 1) * (1 + det) * x) for k, a in enumerate(harm))
for i, ch in enumerate(CHORDS):
    s, n = int(i * bar * SR), int(bar * SR)
    pad = sum(tone(hz(m), n) + tone(hz(m), n, det=.003) for m in ch + [ch[0] + 12])
    out[s:s + n] += .05 * pad * env(n, .45, .6)
    for b in (0, 2):  # bass on beats 1 and 3
        bs, bn = s + int(b * beat * SR), int(2 * beat * SR)
        out[bs:bs + bn] += .16 * tone(hz(ch[0] - 12), bn, (1, .2)) * np.exp(-np.arange(bn) / SR * 2.2)
    for k in range(8):  # arpeggio in eighth notes
        m = (ch + [ch[0] + 12])[[0, 1, 2, 3, 2, 1, 2, 3][k]] + 12
        as_, an = s + int(k * beat / 2 * SR), int(beat / 2 * SR)
        out[as_:as_ + an] += .035 * tone(hz(m), an, (1, .1)) * np.exp(-np.arange(an) / SR * 6)
for b in range(int(len(CHORDS) * 4)):  # kick on 1 and 3, hat on off-beats
    s = int(b * beat * SR)
    if b % 2 == 0:
        kn = int(.28 * SR); x = np.arange(kn) / SR
        out[s:s + kn] += .22 * np.sin(2 * np.pi * (45 + 75 * np.exp(-x * 22)) * x) * np.exp(-x * 14)
    hs = s + int(beat / 2 * SR); hn = int(.035 * SR)
    out[hs:hs + hn] += .02 * np.random.default_rng(b).standard_normal(hn) * np.linspace(1, 0, hn)
out /= np.abs(out).max() * 1.2
root = Path(__file__).resolve().parent.parent; (root / 'assets').mkdir(exist_ok=True)
raw = root / 'assets' / 'bed.raw.wav'; sf.write(raw, np.stack([out, np.roll(out, 220)], 1), SR)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', 'lowpass=f=5500,aecho=0.8:0.6:60|120:0.18|0.12,loudnorm=I=-18:TP=-2', str(root / 'assets' / 'bed.wav')], check=True)
raw.unlink(); print('music bed ->', root / 'assets' / 'bed.wav')

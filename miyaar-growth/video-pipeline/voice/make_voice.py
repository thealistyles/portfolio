#!/usr/bin/env python3
"""Voices every reel with Kokoro (voice/mouth.py), fits the voice to the video, mixes it, and writes captions.txt.
usage: python3 voice/make_voice.py [--voice am_michael] [--only 1,4]"""
import argparse, json, re, subprocess, sys
sys.stdout.reconfigure(line_buffering=True)
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; OUT = ROOT / 'out'; MOUTH = ROOT / 'voice' / 'mouth.py'
ap = argparse.ArgumentParser(); ap.add_argument('--voice', default='af_heart'); ap.add_argument('--speed', type=float, default=1.05)
ap.add_argument('--only'); a = ap.parse_args()
data = json.loads(subprocess.run(['node', '-e', "const c=require('./content/reels.cjs');console.log(JSON.stringify(c))"], cwd=ROOT, capture_output=True, text=True, check=True).stdout)
only = {int(x) for x in a.only.split(',')} if a.only else None
(OUT / 'voice').mkdir(parents=True, exist_ok=True); (OUT / 'final').mkdir(exist_ok=True)
def dur(f): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)], capture_output=True, text=True).stdout)
def say(txt, wav, speed):
    Path(str(wav).replace('.wav', '.txt')).write_text(txt + '\n')
    subprocess.run([sys.executable, str(MOUTH), 'say', str(wav).replace('.wav', '.txt'), str(wav), '--voice', a.voice, '--speed', f'{speed:.3f}', '--words', '--lexicon', str(ROOT / 'voice' / 'lexicon.json')], check=True, capture_output=True)
    return json.loads(Path(str(wav).replace('.wav', '.json')).read_text())
for r in data['reels']:
    if only and r['id'] not in only: continue
    n = f"{r['id']:02d}"; video = OUT / 'silent' / f'reel-{n}.mp4'; wav = OUT / 'voice' / f'reel-{n}.wav'
    if not video.exists(): print(f'reel {n}: no silent video, skipped'); continue
    vd, speed = dur(video), a.speed
    meta = say(r['vo'], wav, speed)
    need = meta['duration'] + 0.3 + 0.6  # voice offset + a breath before the end
    if need > vd:  # keep the natural voice; lengthen the end card and re-render this reel
        fitf = OUT / 'fit.json'; fit = json.loads(fitf.read_text()) if fitf.exists() else {}
        fit[str(r['id'])] = round(fit.get(str(r['id']), 0) + need - vd + 0.05, 2); fitf.write_text(json.dumps(fit, indent=1))
        subprocess.run(['node', 'render.cjs', 'reels', '--only', str(r['id'])], cwd=ROOT, check=True, capture_output=True)
        vd = dur(video)
    heard = ' '.join(w['text'] for w in meta.get('words', []))
    subprocess.run([sys.executable, str(MOUTH), 'mix', str(video), str(wav), str(OUT / 'final' / f'reel-{n}.mp4'), '--offset', '0.3'], check=True, capture_output=True)
    print(f"reel {n}: video {vd:.1f}s voice {meta['duration']:.1f}s speed {speed:.2f}\n  heard: {heard}")
lines = []
for kind in ('reels', 'posts'):
    for x in data[kind]:
        lines += [f"{kind[:-1].upper()} {x['id']:02d}: {x.get('title', '')}", x['caption'], '', x['tags'], '', '----', '']
(OUT / 'captions.txt').write_text('\n'.join(lines))
print('captions ->', OUT / 'captions.txt')

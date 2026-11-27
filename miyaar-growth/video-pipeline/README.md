# Miyaar video pipeline

Turns Miyaar Developers' own photos, renders and plot-to-keys film (from miyaardevelopers.com) into vertical reels with voiceover, plus 4:5 posts. One command, free tools, runs offline after the first download.

```bash
cd miyaar-growth/video-pipeline
./run.sh                         # everything: assets -> posts + reels -> voiceover -> out/
node render.cjs preview          # quick QA stills of every scene (out/qa)
node render.cjs reels --only 3,9 # re-render chosen reels
python3 voice/make_voice.py --voice af_heart --only 3,9   # re-voice with another voice
```

Needs Node with Playwright, Python 3, and ffmpeg. The first voice run downloads the Kokoro voice model (about 120 MB).

## Output (`out/`)

| Folder | What |
|---|---|
| `final/reel-01.mp4` … `reel-15.mp4` | 9:16 reels with voiceover, ready to post |
| `final/reel-16.mp4` | AI plot-to-house film (Canva Locked Transformation). Rendered only when `assets/canva-transformation-aabpara.mp4` is present |
| `posts/post-01.jpg` … `post-15.jpg` | 1080 × 1350 posts |
| `covers/` | Cover frame for each reel |
| `captions.txt` | Caption and hashtags for every reel and post |
| `silent/`, `voice/` | Intermediate files |

## How it works

1. **`fetch_assets.sh`** downloads Miyaar's photos and `plot-to-keys.mp4` from the website into `assets/`.
2. **`content/reels.cjs`** holds every reel as a list of scenes, plus its voiceover script, caption and hashtags. Edit this file to make new reels.
3. **`render.cjs`** opens `engine/studio.html` in headless Chromium, steps through each reel frame by frame at 30 fps, and pipes the frames to ffmpeg. Clip scenes pull their frames from the plot-to-keys film.
4. **`voice/make_voice.py`** reads each script with Kokoro (`voice/mouth.py`, from the `mouth` skill). If a voice runs longer than its video, it speeds it up just enough, up to 1.25×. Then it mixes the voice in at -14 LUFS and writes `captions.txt`.

## Scene types (in `content/reels.cjs`)

| Type | Use | Key fields |
|---|---|---|
| `photo` | A house photo or render with slow pan or zoom; the whole house stays sharp over a blurred fill | `img`, `kb` (`in`, `out`, `left`, `right`, `up`), `text`, optional `num`, `fit: 'cover'` |
| `clip` | A moment from a video in `assets/` | `clip: C(T.steel)` or `{ src, from }`, `text` |
| `card` | A panel over a dimmed background: prices, a list, or a comparison | `card: { kind: 'price' \| 'list' \| 'compare', … }` |
| `cta` | End card with the WhatsApp number and site | `h`, `sub` |

The `text` field takes `{ at: 'top' | 'bottom', k, h, sub, tag, size }`. Wrap words in `==double equals==` to colour them amber.

## Rules the content follows

- **Facts only from Miyaar's own website:** prices, materials, timelines, cities and portfolio. Never invent numbers, reviews or testimonials.
- **Hook in the first 2–3 seconds:** on-screen text plus the strongest shot. Cuts every 1.5–3 seconds, matched to the voiceover.
- **Every reel ends on one action:** WhatsApp, a free estimate, or "comment 1, 2 or 3".
- **Text stays inside the Reels safe area:** top 240 px to bottom 430 px, clear of the right-side buttons.

## Adding an AI transformation film (Canva)

Canva's **Locked Transformation** guide turns one photo of a finished house into a 12-second film: the empty plot fills with sped-up workers and becomes that house. To make one, upload a portfolio photo to Canva, generate the film there, download the MP4 into `assets/`, then use it in a `clip` scene. You can also voice it with `voice/mouth.py mix`.

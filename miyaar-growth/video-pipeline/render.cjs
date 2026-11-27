// Renders posts (JPG) and silent reels (MP4) from content/reels.js using engine/studio.html.
// usage: node render.cjs [all|posts|reels|preview] [--only 1,4,9]
const { chromium } = require('playwright'); const { spawn, execFileSync } = require('child_process');
const fs = require('fs'); const path = require('path');
const ROOT = __dirname, ASSETS = path.join(ROOT, 'assets'), OUT = path.join(ROOT, 'out'), CACHE = path.join(ROOT, 'cache', 'clips');
const { reels, posts } = require('./content/reels.cjs');
const MODE = process.argv[2] || 'all', oi = process.argv.indexOf('--only');
const ONLY = oi > 0 ? process.argv[oi + 1].split(',').map(Number) : null, FPS = 30, pad = n => String(n).padStart(2, '0');
const pick = list => list.filter(x => !ONLY || ONLY.includes(x.id));
function clipFrames(s) { // extract the frames a clip scene needs, once
  const dir = path.join(CACHE, `${path.basename(s.clip.src, '.mp4')}_${s.clip.from}_${s.dur}`);
  if (!fs.existsSync(path.join(dir, 'done'))) {
    fs.mkdirSync(dir, { recursive: true });
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-ss', String(s.clip.from), '-t', String(s.dur + 0.2), '-i', path.join(ASSETS, s.clip.src),
      '-vf', `fps=${FPS},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920`, '-q:v', '3', path.join(dir, '%04d.jpg')]);
    fs.writeFileSync(path.join(dir, 'done'), '');
  }
  return { ...s, clip: 'file://' + dir, frames: fs.readdirSync(dir).filter(f => f.endsWith('.jpg')).length };
}
const prepare = spec => ({ ...spec, scenes: spec.scenes ? spec.scenes.map(s => s.clip ? clipFrames(s) : s) : undefined, ...(spec.clip ? clipFrames(spec) : {}) });
(async () => {
  for (const d of ['silent', 'posts', 'covers', 'qa']) fs.mkdirSync(path.join(OUT, d), { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.join(ROOT, 'engine', 'studio.html'));
  const A = 'file://' + ASSETS;
  if (MODE === 'all' || MODE === 'posts' || MODE === 'preview') {
    await p.setViewportSize({ width: 1080, height: 1350 });
    for (const s of pick(posts)) { await p.evaluate(([s, a]) => setupPost(s, a), [prepare(s), A]); await p.screenshot({ path: `${OUT}/posts/post-${pad(s.id)}.jpg`, type: 'jpeg', quality: 92 }); }
    await p.setViewportSize({ width: 1080, height: 1920 });
  }
  for (const r0 of pick(reels)) {
    if (MODE === 'posts') break;
    const missing = r0.scenes.filter(s => s.clip && !fs.existsSync(path.join(ASSETS, s.clip.src))).map(s => s.clip.src);
    if (missing.length) { console.log(`reel ${r0.id}: skipped, missing assets/${[...new Set(missing)].join(', ')}`); continue; }
    const r = prepare(r0); const dur = await p.evaluate(([s, a]) => setupReel(s, a), [r, A]);
    if (MODE === 'preview') { let t = 0; for (const [i, s] of r.scenes.entries()) { t += s.dur; await p.evaluate(x => seekAsync(x), t - .3); await p.screenshot({ path: `${OUT}/qa/r${pad(r.id)}-s${i}.jpg`, type: 'jpeg', quality: 70 }); } continue; }
    const N = Math.round(dur * FPS), file = `${OUT}/silent/reel-${pad(r.id)}.mp4`;
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', file]);
    for (let f = 0; f < N; f++) { await p.evaluate(x => seekAsync(x), f / FPS); const buf = await p.screenshot({ type: 'jpeg', quality: 90 }); if (!ff.stdin.write(buf)) await new Promise(res => ff.stdin.once('drain', res)); }
    ff.stdin.end(); await new Promise(res => ff.on('close', res));
    await p.evaluate(x => seekAsync(x), r.scenes[0].dur - .2); await p.screenshot({ path: `${OUT}/covers/reel-${pad(r.id)}.jpg`, type: 'jpeg', quality: 88 });
    console.log(`reel ${r.id}: ${dur.toFixed(1)}s`);
  }
  console.log('errors:', errs.length ? errs : 'none'); await b.close();
})();

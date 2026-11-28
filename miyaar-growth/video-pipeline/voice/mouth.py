#!/usr/bin/env python3
"""mouth.py - natural voiceover with Kokoro TTS (free, offline after a 120 MB download).

  voices                              list voices (54; English ones recommended below)
  preview "one line" OUTDIR [--voices am_michael,bm_george,af_heart]   same line, several voices
  say SCRIPT.txt OUT.wav [--voice am_michael] [--speed 1.0] [--lang en-us] [--pause 0.28]
        [--para 0.65] [--lexicon lex.json] [--lufs -16] [--words]
        -> OUT.wav (48 kHz mastered), OUT.json (sentence times; word times with --words)
  mix VIDEO VOICE.wav OUT.mp4 [--music BED.mp3] [--music-db -20] [--keep-original -18]
        voice over a video: music looped and ducked under the voice, -14 LUFS, picture copied
  broll VOICE.json OUT.mp4 CLIP [CLIP ...] [--size 1920x1080] [--fps 30] [--per sentence|N]
        silent B-roll track as long as the voice, cutting on sentence boundaries (faceless video)

Script markup: blank line = paragraph pause; [pause 1.5] = silence; [voice bm_george] and
[speed 0.95] switch from there on; lines starting with # are notes and are not spoken.
Lexicon json {"Lahore": "Lah-hor", "SQL": "sequel"} fixes pronunciation (whole words).
"""
import argparse, json, os, re, subprocess, sys, tarfile, urllib.request
from pathlib import Path

CACHE = Path(os.environ.get("VIDEO_SKILLS_CACHE", Path.home() / ".cache" / "video-skills"))
KOKORO = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
PARAKEET = "sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8"
GOOD = {"am_michael": "US male, warm narrator", "am_fenrir": "US male, deep", "am_puck": "US male, lively",
        "am_onyx": "US male, low and calm", "bm_george": "UK male, documentary", "bm_fable": "UK male, storyteller",
        "af_heart": "US female, best overall", "af_bella": "US female, expressive", "af_nicole": "US female, soft",
        "bf_emma": "UK female, clear", "hf_alpha": "Hindi female", "hm_omega": "Hindi male"}


def sh(cmd, **kw):
    kw.setdefault("text", True)
    r = subprocess.run([str(c) for c in cmd], capture_output=True, **kw)
    if r.returncode:
        sys.exit(f"failed: {' '.join(map(str, cmd))[:200]}\n{r.stderr[-1200:]}")
    return r


def pip(*p):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *p])
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", *p],
                   stderr=subprocess.DEVNULL)


def kokoro():
    try:
        from kokoro_onnx import Kokoro
    except ImportError:
        pip("kokoro-onnx", "soundfile")
        from kokoro_onnx import Kokoro
    d = CACHE / "kokoro"; d.mkdir(parents=True, exist_ok=True)
    for f in ("kokoro-v1.0.int8.onnx", "voices-v1.0.bin"):
        if not (d / f).exists():
            print(f"downloading {f} (once) ...", file=sys.stderr)
            urllib.request.urlretrieve(KOKORO + f, d / f)
    return Kokoro(str(d / "kokoro-v1.0.int8.onnx"), str(d / "voices-v1.0.bin"))


def lang_for(voice):
    return {"a": "en-us", "b": "en-gb", "e": "es", "f": "fr-fr", "h": "hi", "i": "it", "j": "ja",
            "p": "pt-br", "z": "cmn"}.get(voice[0], "en-us")


def parse(script, lex):
    """-> list of ("say", text, voice, speed) | ("pause", seconds)."""
    out, voice, speed = [], None, None
    paras = re.split(r"\n\s*\n", "\n".join(l for l in script.splitlines() if not l.lstrip().startswith("#")))
    for pi, para in enumerate(paras):
        for tok in re.split(r"(\[(?:pause|voice|speed)\s+[^\]]+\])", para):
            m = re.match(r"\[(pause|voice|speed)\s+([^\]]+)\]", tok)
            if m:
                k, v = m.group(1), m.group(2).strip()
                if k == "pause":
                    out.append(("pause", float(v)))
                elif k == "voice":
                    voice = v
                else:
                    speed = float(v)
                continue
            text = " ".join(tok.split())
            for k, v in lex.items():
                text = re.sub(rf"\b{re.escape(k)}\b", v, text)
            for s in re.split(r"(?<=[.!?…])\s+(?=[\"“']?[A-Z0-9$])", text):
                if s.strip():
                    out.append(("say", s.strip(), voice, speed))
                    out.append(("gap", None))
        if out and out[-1][0] == "gap":
            out[-1] = ("para", None)
    return out


def words_for(wav):
    """word times by transcribing the finished voice (Parakeet via sherpa-onnx)."""
    try:
        import sherpa_onnx
    except ImportError:
        pip("sherpa-onnx")
        import sherpa_onnx
    import numpy as np
    d = CACHE / PARAKEET
    if not (d / "tokens.txt").exists():
        tgz = CACHE / f"{PARAKEET}.tar.bz2"
        urllib.request.urlretrieve(f"https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/{PARAKEET}.tar.bz2", tgz)
        with tarfile.open(tgz) as t:
            try:
                t.extractall(CACHE, filter="data")
            except TypeError:
                t.extractall(CACHE)
        tgz.unlink()
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=str(d / "encoder.int8.onnx"), decoder=str(d / "decoder.int8.onnx"), joiner=str(d / "joiner.int8.onnx"),
        tokens=str(d / "tokens.txt"), num_threads=4, model_type="nemo_transducer")
    raw = sh(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], text=False).stdout
    x, words, step = np.frombuffer(raw, np.float32), [], 16000 * 25
    for a in range(0, len(x), step):
        s = rec.create_stream(); s.accept_waveform(16000, x[a:a + step + 16000 * 2] if a + step < len(x) else x[a:])
        rec.decode_stream(s); r, off, fresh = s.result, a / 16000, True
        durs = list(getattr(r, "durations", []) or [])
        for i, (tok, t) in enumerate(zip(r.tokens, r.timestamps)):
            if a + step < len(x) and t >= 25.0:
                break  # the overlap belongs to the next chunk
            st, dur = tok.strip(), durs[i] if i < len(durs) else 0.08
            if not st:
                continue
            if re.fullmatch(r"[.,!?;:%)\]}\"”’…\-–]+", st) and not fresh:
                words[-1]["text"] += st
            elif tok.startswith(" ") or fresh or (re.match(r"[\d$€£₹]", st) and re.search(r"[A-Za-z.!?]$", words[-1]["text"])):
                words.append({"text": st, "start": round(off + t, 3), "end": round(off + t + dur, 3)}); fresh = False
            else:
                words[-1]["text"] += st; words[-1]["end"] = round(off + t + dur, 3)
    for i in range(len(words) - 1):
        words[i]["end"] = min(words[i]["end"], words[i + 1]["start"])
    return words


def master(src, dst, lufs):
    chain = "aresample=48000,highpass=f=70,acompressor=threshold=-21dB:ratio=2.2:attack=8:release=120:makeup=1.5"
    e = sh(["ffmpeg", "-hide_banner", "-i", src, "-af", f"{chain},loudnorm=I={lufs}:TP=-1.5:LRA=7:print_format=json",
            "-f", "null", "-"]).stderr
    m = json.loads(e[e.rindex("{"):e.rindex("}") + 1])
    ln = (f"loudnorm=I={lufs}:TP=-1.5:LRA=7:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    sh(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", f"{chain},{ln},aresample=48000", "-c:a", "pcm_s16le", dst])


def say(a):
    import numpy as np, soundfile as sf
    k = kokoro()
    lex = json.load(open(a.lexicon)) if a.lexicon else {}
    items = parse(Path(a.script).read_text(encoding="utf-8"), lex)
    sr, pieces, t, sents = 24000, [], 0.0, []
    for it in items:
        if it[0] == "say":
            _, text, v, s = it
            voice, speed = v or a.voice, s or a.speed
            audio, sr = k.create(text, voice=voice, speed=speed, lang=a.lang or lang_for(voice))
            pieces.append(audio.astype(np.float32))
            sents.append({"text": text, "voice": voice, "start": round(t, 3), "end": round(t + len(audio) / sr, 3)})
            t += len(audio) / sr
        else:
            sec = it[1] if it[0] == "pause" else (a.para if it[0] == "para" else a.pause)
            pieces.append(np.zeros(int(sec * sr), np.float32)); t += sec
    raw = Path(a.out).with_suffix(".raw.wav")
    sf.write(raw, np.concatenate(pieces) if pieces else np.zeros(sr, np.float32), sr)
    master(raw, a.out, a.lufs); raw.unlink()
    meta = {"voice": a.voice, "speed": a.speed, "duration": round(t, 2), "sentences": sents}
    if a.words:
        meta["words"] = words_for(a.out)
    json.dump(meta, open(Path(a.out).with_suffix(".json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"wav": a.out, "duration": meta["duration"], "sentences": len(sents),
                      "words": len(meta.get("words", [])), "timing": str(Path(a.out).with_suffix(".json"))}))


def mix(a):
    v = json.loads(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", a.video]).stdout)
    vd = float(v["format"]["duration"])
    vo = float(json.loads(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json",
                              a.voice]).stdout)["format"]["duration"])
    has_a = "audio" in sh(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", a.video]).stdout
    ins, mixin = ["-i", a.video, "-i", a.voice], ["[vo]"]
    fl = [f"[1:a]aresample=48000,adelay={int(a.offset * 1000)}:all=1,apad[v0]"]
    if a.music:
        ins += ["-stream_loop", "-1", "-i", a.music]
        fl += [f"[2:a]aresample=48000,volume={a.music_db}dB,afade=t=in:d=1.5,afade=t=out:st={max(0, vd - 2.5):.2f}:d=2.5[mus]",
               "[v0]asplit=2[vo][key]", "[mus][key]sidechaincompress=threshold=0.04:ratio=10:attack=15:release=450[duck]"]
        mixin.append("[duck]")
    else:
        fl.append("[v0]anull[vo]")
    if a.keep_original is not None and has_a:
        fl.append(f"[0:a]aresample=48000,volume={a.keep_original}dB[orig]"); mixin.append("[orig]")
    fl.append("".join(mixin) + f"amix=inputs={len(mixin)}:normalize=0:duration=first,atrim=0:{vd:.3f}[pre]")
    tmp = Path(a.out).with_suffix(".tmp.wav")
    sh(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", ";".join(fl), "-map", "[pre]", "-t", f"{vd:.3f}", tmp])
    master(tmp, str(tmp) + ".m.wav", -14)
    sh(["ffmpeg", "-y", "-v", "error", "-i", a.video, "-i", str(tmp) + ".m.wav", "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", a.out])
    tmp.unlink(); Path(str(tmp) + ".m.wav").unlink()
    print(json.dumps({"out": a.out, "video_s": round(vd, 2), "voice_s": round(vo + a.offset, 2),
                      "warning": f"voice runs {vo + a.offset - vd:.1f} s past the video end and was cut"
                      if vo + a.offset > vd + 0.7 else None}))


def broll(a):
    meta = json.load(open(a.voice_json))
    total, sents = meta["duration"], meta["sentences"]
    group = 1 if a.per == "sentence" else max(1, int(a.per))
    cuts = [s["end"] for s in sents][group - 1::group][:-1] if sents else []
    bounds = [0.0] + [c for c in cuts if 0.8 < c < total - 0.8] + [total]
    w, h = a.size.split("x")
    dur = {c: float(json.loads(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json",
                                   c]).stdout)["format"]["duration"]) for c in a.clips}
    tmp = Path(a.out).with_suffix(".parts"); tmp.mkdir(exist_ok=True)
    lst, k = [], 0
    for t0, t1 in zip(bounds, bounds[1:]):
        left = t1 - t0
        while left > 0.04:  # a clip shorter than the sentence: cut to the next clip, never loop
            clip = a.clips[k % len(a.clips)]
            piece = min(left, dur[clip] - 0.05)
            if left - piece < 0.6:
                piece = left if dur[clip] - 0.05 >= left else piece
            off = (k * 1.7) % max(0.01, dur[clip] - piece) if dur[clip] - piece > 0.3 else 0
            part = tmp / f"p{len(lst):03d}.mp4"
            sh(["ffmpeg", "-y", "-v", "error", "-ss", f"{off:.2f}", "-i", clip, "-t", f"{piece:.3f}", "-vf",
                f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={a.fps},setsar=1,format=yuv420p,"
                f"tpad=stop_mode=clone:stop_duration=1", "-t", f"{piece:.3f}", "-an", "-c:v", "libx264",
                "-preset", "veryfast", "-crf", "19", part])
            lst.append(f"file '{part.resolve()}'"); left -= piece; k += 1
    (tmp / "list.txt").write_text("\n".join(lst))
    sh(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", tmp / "list.txt", "-c", "copy", a.out])
    for p in tmp.iterdir():
        p.unlink()
    tmp.rmdir()
    print(json.dumps({"out": a.out, "shots": len(lst), "duration": round(total, 2)}))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("voices")
    p = sp.add_parser("preview"); p.add_argument("text"); p.add_argument("outdir")
    p.add_argument("--voices", default="am_michael,bm_george,am_fenrir,af_heart"); p.add_argument("--speed", type=float, default=1.0)
    s = sp.add_parser("say"); s.add_argument("script"); s.add_argument("out")
    s.add_argument("--voice", default="am_michael"); s.add_argument("--speed", type=float, default=1.0)
    s.add_argument("--lang"); s.add_argument("--pause", type=float, default=0.28); s.add_argument("--para", type=float, default=0.65)
    s.add_argument("--lexicon"); s.add_argument("--lufs", type=float, default=-16); s.add_argument("--words", action="store_true")
    m = sp.add_parser("mix"); m.add_argument("video"); m.add_argument("voice"); m.add_argument("out")
    m.add_argument("--music"); m.add_argument("--music-db", type=float, default=-20)
    m.add_argument("--keep-original", type=float); m.add_argument("--offset", type=float, default=0.0)
    b = sp.add_parser("broll"); b.add_argument("voice_json"); b.add_argument("out"); b.add_argument("clips", nargs="+")
    b.add_argument("--size", default="1920x1080"); b.add_argument("--fps", type=int, default=30); b.add_argument("--per", default="sentence")
    a = ap.parse_args()
    if a.cmd == "broll":
        return broll(a)
    if a.cmd == "voices":
        names = kokoro().get_voices()
        print(json.dumps({"recommended": {n: d for n, d in GOOD.items() if n in names}, "all": names}, indent=1))
    elif a.cmd == "preview":
        import soundfile as sf
        k, od = kokoro(), Path(a.outdir); od.mkdir(parents=True, exist_ok=True)
        for v in a.voices.split(","):
            audio, sr = k.create(a.text, voice=v, speed=a.speed, lang=lang_for(v))
            sf.write(od / f"{v}.raw.wav", audio, sr); master(od / f"{v}.raw.wav", od / f"{v}.wav", -16)
            (od / f"{v}.raw.wav").unlink(); print(od / f"{v}.wav")
    elif a.cmd == "say":
        say(a)
    else:
        mix(a)


if __name__ == "__main__":
    main()

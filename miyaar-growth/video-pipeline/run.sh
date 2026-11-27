#!/usr/bin/env bash
# One command: assets -> posts + silent reels -> voiceover -> out/final (reels) and out/posts.
set -euo pipefail
cd "$(dirname "$0")"
./fetch_assets.sh
python3 -c "import kokoro_onnx, soundfile" 2>/dev/null || pip install -q kokoro-onnx soundfile sherpa-onnx || pip install -q --break-system-packages kokoro-onnx soundfile sherpa-onnx
node render.cjs all "$@"
python3 voice/make_voice.py
echo "Done: out/final (15 voiced reels), out/posts (15 posts), out/captions.txt"

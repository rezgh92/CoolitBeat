#!/usr/bin/env bash
# Encode the rendered frames and the narration master into the final MP4 (H.264 high profile, AAC) and a smaller preview.
# usage: bash encode.sh <frames_dir> <out.mp4> [fps]
set -euo pipefail
FR=${1:?frames dir}; OUT=${2:?output mp4}; FPS=${3:-30}
HERE=$(cd "$(dirname "$0")" && pwd)
AUD="$HERE/audio/narration_master.wav"
N=$(ls "$FR"/*.jpg | wc -l); echo "frames: $N"
ffmpeg -y -loglevel error -framerate "$FPS" -i "$FR/%06d.jpg" -i "$AUD" \
  -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -profile:v high -level 4.1 -movflags +faststart \
  -c:a aac -b:a 160k -ar 48000 -shortest "$OUT"
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of default=nw=1 "$OUT"

#!/usr/bin/env python3
"""Synthesise the narration per scene with piper and write timeline.json (scene start/end in seconds, frame counts).
usage: python3 narrate.py [--voice path/to/model.onnx] [--out audio/]"""
import argparse, json, pathlib, subprocess, wave, struct, math
HERE = pathlib.Path(__file__).resolve().parent
ap = argparse.ArgumentParser(); ap.add_argument("--voice", required=True); ap.add_argument("--out", default=str(HERE / "audio"))
a = ap.parse_args()
S = json.load(open(HERE / "script.json")); out = pathlib.Path(a.out); out.mkdir(exist_ok=True)
fps = S["fps"]; t = 0.0; timeline = []
for sc in S["scenes"]:
    wav = out / f"{sc['id']}.wav"
    subprocess.run(["piper", "--model", a.voice, "--output_file", str(wav), "--sentence-silence", "0.35", "--length-scale", "1.04"],
                   input=sc["narration"].encode(), check=True, capture_output=True)
    w = wave.open(str(wav)); dur = w.getnframes() / w.getframerate(); rate = w.getframerate(); w.close()
    length = max(sc["min_s"], dur + sc["pad_s"])
    length = math.ceil(length * fps) / fps
    timeline.append({"id": sc["id"], "start": round(t, 4), "end": round(t + length, 4), "narration_s": round(dur, 3), "frames": int(round(length * fps))})
    t += length
json.dump({"fps": fps, "total_s": round(t, 3), "total_frames": int(round(t * fps)), "rate": rate, "scenes": timeline}, open(HERE / "timeline.json", "w"), indent=1)
# master narration track: each scene's wav placed at its start, 0.6 s after the scene begins
import array
master = array.array("h", [0] * int(t * rate + rate))
for sc in timeline:
    w = wave.open(str(out / f"{sc['id']}.wav")); frames = w.readframes(w.getnframes()); w.close()
    data = array.array("h"); data.frombytes(frames)
    off = int((sc["start"] + 0.6) * rate)
    for i, v in enumerate(data):
        if off + i < len(master): master[off + i] = max(-32768, min(32767, master[off + i] + v))
mw = wave.open(str(out / "narration_master.wav"), "wb"); mw.setnchannels(1); mw.setsampwidth(2); mw.setframerate(rate); mw.writeframes(master.tobytes()); mw.close()
print(json.dumps({"total_s": round(t, 1), "frames": int(round(t * fps)), "scenes": [(s["id"], s["narration_s"], s["end"] - s["start"]) for s in timeline]}, indent=0))

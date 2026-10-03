#!/usr/bin/env python3
"""Cut the intro video into the frame sequence the hero card plays.

    python3 tools/profile-art/make_frames.py            # reads graywizard.mp4
    python3 tools/profile-art/make_frames.py --help

GitHub strips <video>/<iframe> from READMEs, so a real video cannot play there.
The hero card fakes one instead: every frame is embedded in the SVG as a data
URI and a CSS animation with `iteration-count: 1` + `fill-mode: forwards` shows
them in order, then holds on the last frame. That is how the card "plays once"
and then sits on its play button.

This script is a DEVELOPMENT tool - it needs ffmpeg (installed automatically via
`pip install imageio-ffmpeg`). `build.py` only *reads* the frames it writes, so
the daily refresh workflow never needs ffmpeg.

Settings are deliberately modest: the frames are still images, so there is no
temporal compression and the whole sequence lands inside hero.svg. 400x225 at
8 fps keeps the card near 900 KB; the card draws it at 480x270 (a 1.2x upscale,
which video content carries fine).

Re-run it only when the source video changes, then run build.py.
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "assets", "intro")

DEFAULTS = dict(fps=8, width=400, height=225, quality=30, source="graywizard.mp4", poster=0)


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        exe = shutil.which("ffmpeg")
        if not exe:
            sys.exit("ffmpeg not found - pip install imageio-ffmpeg")
        return exe


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=DEFAULTS["source"], help="video file, relative to the repo root")
    ap.add_argument("--fps", type=int, default=DEFAULTS["fps"])
    ap.add_argument("--width", type=int, default=DEFAULTS["width"])
    ap.add_argument("--height", type=int, default=DEFAULTS["height"])
    ap.add_argument("--quality", type=int, default=DEFAULTS["quality"],
                    help="libwebp quality (25-40 is the useful range here)")
    ap.add_argument("--poster", type=int, default=DEFAULTS["poster"],
                    help="frame index used as the still/poster (0 = the video's first frame)")
    ap.add_argument("--out", default="assets/intro",
                    help="output directory, relative to the repo root "
                         "(the phones' lighter cut lives in assets/intro/mobile)")
    args = ap.parse_args()

    src = os.path.join(ROOT, args.source)
    if not os.path.exists(src):
        sys.exit(f"no such video: {src}")

    out = os.path.join(ROOT, args.out)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    exe = ffmpeg()
    cmd = [exe, "-y", "-i", src,
           "-vf", f"fps={args.fps},scale={args.width}:{args.height}",
           "-c:v", "libwebp", "-quality", str(args.quality), "-compression_level", "6",
           os.path.join(out, "f%03d.webp"), "-hide_banner", "-loglevel", "error"]
    subprocess.run(cmd, check=True)

    frames = sorted(glob.glob(os.path.join(out, "*.webp")))
    if not frames:
        sys.exit("no frames were written")
    duration = len(frames) / args.fps
    poster = frames[min(max(args.poster, 0), len(frames) - 1)]
    shutil.copy(poster, os.path.join(out, "poster.webp"))

    meta = {
        "frames": len(frames),
        "fps": args.fps,
        "duration": round(duration, 3),
        "stored": f"{args.width}x{args.height}",
        "quality": args.quality,
        "source": args.source,
        "poster": os.path.basename(poster),
    }
    with open(os.path.join(out, "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")

    total = sum(os.path.getsize(f) for f in frames)
    print(f"{len(frames)} frames @ {args.fps} fps = {duration:.1f}s, {args.width}x{args.height}, q{args.quality}")
    print(f"frames total {total/1024:.0f} KB, poster = {meta['poster']}")
    print(f"written to {os.path.relpath(out, ROOT)}/")


if __name__ == "__main__":
    main()

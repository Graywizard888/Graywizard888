"""The intro "video" panel for the hero cards.

GitHub strips <video>, <iframe> and every other real player out of a README, so
the hero fakes one: `make_frames.py` cuts the source clip into stills, this
module embeds them as data URIs and a CSS animation with
`animation-iteration-count: 1` + `fill-mode: forwards` shows them in order and
then HOLDS on the last frame. After the sequence ends the play button fades back
in over the centre.

Two modes, one drawing:

    "play"    all frames + the one-shot animation (desktop)
    "poster"  the poster frame only, play button showing (phones)

Everything that cannot animate (phones, `prefers-reduced-motion`, resvg, any
renderer without CSS) falls back to the poster state, so the card is never
broken - it just shows the frame and the play button, which is exactly the
"finished" state the animation settles on.

Timing is driven by assets/intro/meta.json, so re-cutting the video at a
different length or frame rate changes nothing here.
"""
import base64
import json
import os

from gen_common import CYAN, DIM, GREEN, GREEN_D, MUTED, STROKE

HERE = os.path.dirname(os.path.abspath(__file__))
FRAME_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "assets", "intro"))

VIDEO_W, VIDEO_H = 480, 270     # displayed size in the card
PAD = 26                        # window padding either side of the video
TITLE_H = 42                    # window top -> video top
BELOW = 54                      # video bottom -> window bottom
WINDOW_W = VIDEO_W + PAD * 2    # 532
WINDOW_H = TITLE_H + VIDEO_H + BELOW

_cache = {}


def load():
    """(base64 frames, meta) - read once per process, empty on a missing asset."""
    if "frames" in _cache:
        return _cache["frames"], _cache["meta"]
    frames, meta = [], {"frames": 0, "fps": 8, "duration": 0.0}
    if os.path.isdir(FRAME_DIR):
        with open(os.path.join(FRAME_DIR, "meta.json"), encoding="utf-8") as fh:
            meta = json.load(fh)
        for i in range(1, meta["frames"] + 1):
            path = os.path.join(FRAME_DIR, f"f{i:03d}.webp")
            with open(path, "rb") as fh:
                frames.append(base64.b64encode(fh.read()).decode())
        poster_path = os.path.join(FRAME_DIR, meta.get("poster", "poster.webp"))
        if os.path.exists(poster_path):
            with open(poster_path, "rb") as fh:
                meta["poster_b64"] = base64.b64encode(fh.read()).decode()
    _cache["frames"], _cache["meta"] = frames, meta
    return frames, meta


def video_css(meta):
    """Per-frame `opacity` keyframes: frame i owns the slot [i, i+1) of the run.

    `steps(1, end)` makes each keyframe hold until the next one, so the frames
    cut over hard instead of cross-fading. The first frame is visible in the
    base style and the last one holds forever, which is what makes the static
    fallback show frame 0 and the finished state show frame N.
    """
    n = max(1, meta["frames"])
    slot = 100.0 / n
    out = ["\n  /* --- intro video: one-shot frame sequence, holds on the last frame --- */",
           ".vfr { opacity: 0; animation-duration: %.3fs; animation-iteration-count: 1;"
           " animation-fill-mode: forwards; animation-timing-function: steps(1, end); }"
           % meta["duration"]]
    out.append(".vfr0 { opacity: 1; animation-name: vf0; }")
    for i in range(1, n):
        out.append(f".vfr{i} {{ animation-name: vf{i}; }}")
    for i in range(n):
        start, end = i * slot, (i + 1) * slot
        if i == 0:
            out.append(f"@keyframes vf0 {{ 0% {{ opacity: 1 }} {end:.4f}% {{ opacity: 0 }} 100% {{ opacity: 0 }} }}")
        elif i == n - 1:
            out.append(f"@keyframes vf{i} {{ 0% {{ opacity: 0 }} {start:.4f}% {{ opacity: 1 }} 100% {{ opacity: 1 }} }}")
        else:
            out.append(f"@keyframes vf{i} {{ 0% {{ opacity: 0 }} {start:.4f}% {{ opacity: 1 }}"
                       f" {end:.4f}% {{ opacity: 0 }} 100% {{ opacity: 0 }} }}")
    end = meta["duration"]
    out.append(
        # the shade + play button belong to the paused state: they fade out when
        # playback starts and come back when it ends (fill `both` hides them
        # during the delay, which plain `forwards` would not)
        "\n  /* paused state: dimmed poster before and after, clear while playing */\n"
        f"  .vshade {{ opacity: .42; animation: vshade {end + 0.6:.2f}s linear 1 forwards; }}\n"
        f"  .vplay {{ opacity: 1; animation: vplayin .55s ease-out {end + 0.05:.2f}s 1 both; }}\n"
        f"  @keyframes vshade {{ 0% {{ opacity: .42 }} {0.4 / (end + 0.6) * 100:.2f}% {{ opacity: 0 }}"
        f" {end / (end + 0.6) * 100:.2f}% {{ opacity: 0 }} 100% {{ opacity: .42 }} }}\n"
        "  @keyframes vplayin { 0% { opacity: 0 } 100% { opacity: 1 } }\n"
        # labels: the ended one shows only after, the playing one only during
        f"  .vended {{ opacity: 1; animation: vended .3s linear {end + 0.05:.2f}s 1 both; }}\n"
        f"  .vplaying {{ opacity: 0; animation: vplaying {end + 0.15:.2f}s linear 1 forwards; }}\n"
        "  @keyframes vended { 0% { opacity: 0 } 100% { opacity: 1 } }\n"
        f"  @keyframes vplaying {{ 0% {{ opacity: 1 }} {end / (end + 0.15) * 100:.2f}% {{ opacity: 1 }}"
        " 100% { opacity: 0 } }\n"
        # progress bar: a dashed line drawn on by dashoffset (no transform-origin
        # games, which are the flakiest part of SVG+CSS)
        f"  .vprog {{ stroke-dashoffset: {VIDEO_W}; animation: vgrow {end:.2f}s linear 1 forwards; }}\n"
        f"  @keyframes vgrow {{ to {{ stroke-dashoffset: 0 }} }}\n"
        # the blinking cursor stops with the sequence instead of running forever
        "  .vblink { opacity: 0; animation: vblink 1s steps(1, end) 1 forwards,"
        f" vdot {end + 0.15:.2f}s step-end 1 forwards; }}\n"
        "  @keyframes vblink { 0%, 50% { opacity: 1 } }\n"
        "  @keyframes vdot { 0% { opacity: 1 } 100% { opacity: 0 } }"
    )
    return "\n  ".join(out) + "\n"


def _frames_layer(x, y, frames, meta, animated):
    """The picture itself: every frame stacked, only one visible at a time."""
    out = [f'<clipPath id="vClip"><rect x="{x}" y="{y}" width="{VIDEO_W}" height="{VIDEO_H}" rx="8"/></clipPath>']
    imgs = []
    if animated and frames:
        for i, b64 in enumerate(frames):
            cls = f"vfr vfr{i}" if i else "vfr vfr0"
            imgs.append(f'<image class="{cls}" x="{x}" y="{y}" width="{VIDEO_W}" height="{VIDEO_H}"'
                        f' preserveAspectRatio="xMidYMid slice" href="data:image/webp;base64,{b64}"/>')
    else:
        b64 = meta.get("poster_b64") or (frames[0] if frames else None)
        if b64:
            imgs.append(f'<image x="{x}" y="{y}" width="{VIDEO_W}" height="{VIDEO_H}"'
                        f' preserveAspectRatio="xMidYMid slice" href="data:image/webp;base64,{b64}"/>')
        else:   # assets missing: say so instead of drawing an empty hole
            imgs.append(f'<rect x="{x}" y="{y}" width="{VIDEO_W}" height="{VIDEO_H}" fill="#0a1119"/>')
            imgs.append(f'<text x="{x + VIDEO_W/2}" y="{y + VIDEO_H/2}" fill="{MUTED}" font-size="15"'
                        f' text-anchor="middle" class="fm">// no signal - run make_frames.py</text>')
    # one <image> per line: the file stays diffable even at ~11 KB per frame
    out.append(f'<g clip-path="url(#vClip)">\n' + "\n".join(imgs) + "\n</g>")
    return out


def panel(x, y, mode="play"):
    """Draw the player window with its top-left corner at (x, y).

    Returns (body, css, defs, height). `body` slots into the card between the
    HUD strip and the rest of the layout; `css` goes into the card's <style>.
    """
    animated = mode == "play"
    frames, meta = load()
    vx, vy = x + PAD, y + TITLE_H
    mid_x, mid_y = vx + VIDEO_W / 2, vy + VIDEO_H / 2
    bar_y = vy + VIDEO_H + 16
    status_y = bar_y + 26
    label = (f"▸ PLAYING · {meta['fps']} fps · silent" if animated
             else f"▸ INTRO · {meta['duration']:.0f}s · silent")

    body = [
        # soft glow so the window reads as lit from behind
        f'<ellipse cx="{x + WINDOW_W/2}" cy="{y + WINDOW_H/2}" rx="{WINDOW_W*0.62:.0f}"'
        f' ry="{WINDOW_H*0.72:.0f}" fill="url(#vGlow)"/>',
        f'<rect x="{x}" y="{y}" width="{WINDOW_W}" height="{WINDOW_H}" rx="14" fill="url(#vWin)"/>',
        f'<rect x="{x + 1}" y="{y + 1}" width="{WINDOW_W - 2}" height="{WINDOW_H - 2}" rx="13"'
        f' fill="none" stroke="{STROKE}" stroke-width="1.3"/>',
        # title bar
        f'<line x1="{x + 1}" y1="{y + 30}" x2="{x + WINDOW_W - 1}" y2="{y + 30}" stroke="#182838" stroke-width="1"/>',
        f'<circle cx="{x + 20}" cy="{y + 16}" r="5" fill="#ff6b60"/>',
        f'<circle cx="{x + 36}" cy="{y + 16}" r="5" fill="#fbbf24"/>',
        f'<circle cx="{x + 52}" cy="{y + 16}" r="5" fill="#28c840"/>',
        f'<text x="{x + 74}" y="{y + 21}" fill="{MUTED}" font-size="12" class="fm"'
        f' letter-spacing="1.1">// intro.play — graywizard.mp4</text>',
        f'<text x="{x + WINDOW_W - 18}" y="{y + 21}" fill="{DIM}" font-size="12" class="fm"'
        f' text-anchor="end">{meta["duration"]:.1f}s · {meta["frames"]} frames</text>',
    ]
    if animated:
        body.append(f'<circle class="vplaying vblink" cx="{x + WINDOW_W - 92}" cy="{y + 16}" r="4.5" fill="{GREEN}"/>')
        body.append(f'<text class="vplaying fm" x="{x + WINDOW_W - 82}" y="{y + 21}" fill="{GREEN}"'
                    f' font-size="11.5" letter-spacing="1.4">LIVE</text>')
    body += _frames_layer(vx, vy, frames, meta, animated)
    # scanlines + a light vignette keep the video inside the console's look
    body.append(f'<rect x="{vx}" y="{vy}" width="{VIDEO_W}" height="{VIDEO_H}" rx="8" fill="url(#vScan)" opacity=".3"/>')
    # paused shade
    body.append(f'<rect class="{"vshade" if animated else ""}" x="{vx}" y="{vy}" width="{VIDEO_W}"'
                f' height="{VIDEO_H}" rx="8" fill="#03060a" opacity=".42"/>')
    # the play button: visible in the poster state, and again once the video ends
    body += [
        f'<g class="{"vplay" if animated else ""}" transform="translate({mid_x},{mid_y})">',
        f'<circle r="40" fill="#050a10" opacity=".72"/>',
        f'<circle r="40" fill="none" stroke="{GREEN}" stroke-width="2" opacity=".85"/>',
        f'<circle r="31" fill="none" stroke="{GREEN_D}" stroke-width="1" opacity=".3"/>',
        f'<path d="M -11 -17 L 22 0 L -11 17 Z" fill="{GREEN}"/>',
        "</g>",
    ]
    # progress bar + labels
    body += [
        f'<line x1="{vx}" y1="{bar_y}" x2="{vx + VIDEO_W}" y2="{bar_y}" stroke="#16222e"'
        f' stroke-width="6" stroke-linecap="round"/>',
        f'<line class="{"vprog" if animated else ""}" x1="{vx}" y1="{bar_y}" x2="{vx + VIDEO_W}" y2="{bar_y}"'
        f' stroke="url(#vBar)" stroke-width="6" stroke-linecap="round"'
        f' stroke-dasharray="{VIDEO_W}" stroke-dashoffset="{0 if not animated else VIDEO_W}"/>',
        f'<text x="{vx}" y="{status_y}" fill="{DIM}" font-size="12.5" class="fm" letter-spacing="1">{label}</text>',
    ]
    if animated:
        body.append(f'<text class="vended fm" x="{vx}" y="{status_y}" fill="{GREEN}" font-size="12.5"'
                    f' letter-spacing="1.2">▸ ENDED — TAP THE CARD TO PLAY IT AGAIN</text>')
        body.append(f'<text class="vended fm" x="{vx + VIDEO_W}" y="{status_y}" fill="{MUTED}" font-size="12.5"'
                    f' text-anchor="end" letter-spacing="1">00:{meta["duration"]:04.1f}</text>')
    else:
        body.append(f'<text x="{vx + VIDEO_W}" y="{status_y}" fill="{MUTED}" font-size="12.5"'
                    f' text-anchor="end" class="fm" letter-spacing="1">00:{meta["duration"]:04.1f}</text>')

    defs = [
        '<linearGradient id="vWin" x1="0" y1="0" x2=".5" y2="1">'
        '<stop offset="0" stop-color="#0d1721"/><stop offset="1" stop-color="#060b11"/></linearGradient>',
        '<linearGradient id="vBar" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>',
        '<radialGradient id="vGlow" cx=".5" cy=".5" r=".5">'
        f'<stop offset="0" stop-color="{CYAN}" stop-opacity=".13"/>'
        f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>',
        '<pattern id="vScan" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#000" opacity=".6"/></pattern>',
    ]
    css = video_css(meta) if animated else ""
    return "\n".join(body), css, defs, WINDOW_H

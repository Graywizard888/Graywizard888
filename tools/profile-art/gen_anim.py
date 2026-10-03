"""Animation CSS + typed-line helper. Pure CSS/SVG (GitHub-safe: no scripts)."""
from gen_common import T, G, esc, MONO

CSS_VARS = f"""
  .mono-label {{ letter-spacing: 1.4px; }}

  /* rain columns: each column holds 3 stacked blocks of `period`, so a
     translate of exactly one period loops seamlessly */
  .rain {{ animation-name: fall; animation-timing-function: linear;
           animation-iteration-count: infinite; }}
  @keyframes fall {{ from {{ transform: translateY(-470px); }} to {{ transform: translateY(0px); }} }}

  .breathe {{ animation: breathe 3.4s ease-in-out infinite; }}
  @keyframes breathe {{ 0%,100% {{ opacity: .34; }} 50% {{ opacity: .85; }} }}

  .pulse {{ animation: pulse 2.2s ease-in-out infinite; }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}

  .pulse-soft {{ animation: pulseSoft 4s ease-in-out infinite; }}
  @keyframes pulseSoft {{ 0%,100% {{ opacity: .18; }} 50% {{ opacity: .5; }} }}

  .blink {{ animation: blink 1.05s steps(1,end) infinite; }}
  @keyframes blink {{ 0%,49% {{ opacity: 1; }} 50%,100% {{ opacity: 0; }} }}

  .caret-in {{ animation: caretIn .1s steps(1,end) both; }}
  @keyframes caretIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}

  .sweep {{ animation: sweep 7.5s ease-in-out infinite; }}
  @keyframes sweep {{ 0% {{ transform: translateY(-170px); }} 100% {{ transform: translateY(480px); }} }}

  /* bars grow from their own origin: the animated element sits inside a
     translated group, so 0 0 is the bar's left/top corner */
  .grow-x {{ animation-name: growx; animation-timing-function: cubic-bezier(.22,.8,.2,1);
             animation-fill-mode: both; transform-origin: 0px 0px; }}
  @keyframes growx {{ from {{ transform: scaleX(.001); }} to {{ transform: scaleX(1); }} }}

  .eq {{ animation: eq 1.05s ease-in-out infinite; transform-origin: 0px 0px; }}
  @keyframes eq {{ 0%,100% {{ transform: scaleY(.22); }} 50% {{ transform: scaleY(1); }} }}

  .draw {{ animation: dashIn 2.4s cubic-bezier(.3,.9,.25,1) both; }}
  @keyframes dashIn {{ from {{ stroke-dashoffset: var(--len); }} to {{ stroke-dashoffset: 0; }} }}

  .fade-up {{ animation: fadeUp 1s cubic-bezier(.22,.8,.2,1) both; }}
  @keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(10px); }}
                       to {{ opacity: 1; transform: translateY(0); }} }}

  .fade-in {{ animation: fadeIn 1.1s ease-out both; }}
  @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}

  .float {{ animation: float 6s ease-in-out infinite; }}
  @keyframes float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-7px); }} }}

  .float2 {{ animation: float2 8.5s ease-in-out infinite; }}
  @keyframes float2 {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(6px,-9px); }} }}

  .marquee-l {{ animation: marqL 52s linear infinite; }}
  @keyframes marqL {{ from {{ transform: translateX(0); }} to {{ transform: translateX(var(--shift)); }} }}
  .marquee-r {{ animation: marqR 58s linear infinite; }}
  @keyframes marqR {{ from {{ transform: translateX(var(--shift)); }} to {{ transform: translateX(0); }} }}

  /* character-by-character typing: a clip rect steps across the line */
  .typing {{ animation-name: typew; animation-timing-function: steps(var(--steps), end);
             animation-fill-mode: both; }}
  @keyframes typew {{ from {{ transform: translateX(calc(var(--w) * -1)); }}
                      to {{ transform: translateX(0); }} }}

  /* rolling odometer digits */
  .odo {{ animation-name: roll; animation-timing-function: cubic-bezier(.16,.84,.24,1);
          animation-fill-mode: both; transform-origin: 0px 0px; }}
  @keyframes roll {{ from {{ transform: translateY(calc(var(--rows) * var(--lh))); }}
                     to {{ transform: translateY(0); }} }}

  .shine {{ animation: shine 6.5s ease-in-out infinite; }}
  @keyframes shine {{ 0% {{ transform: translateX(-320px); }}
                      55%,100% {{ transform: translateX(1500px); }} }}

  .holo {{ animation: holo 5.5s ease-in-out infinite; }}
  @keyframes holo {{ 0% {{ transform: translateX(-460px) skewX(-16deg); }}
                     45%,100% {{ transform: translateX(760px) skewX(-16deg); }} }}

  .spin {{ animation: spin 26s linear infinite; transform-origin: 0px 0px; }}
  @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

  .drift {{ animation: drift 12s ease-in-out infinite; }}
  @keyframes drift {{ 0%,100% {{ transform: translateX(0); }} 50% {{ transform: translateX(5px); }} }}
"""


def style_block(extra=""):
    return "<style>" + CSS_VARS + extra + "</style>"


def typing_line(cid, x, baseline, text, size, color, width, delay, dur=1.0,
                weight=400, family=MONO, ls=None):
    """Returns (defs_fragment, body_fragment). The clip rect sweeps left->right."""
    steps = max(2, len(text))
    clip = (f'<clipPath id="{cid}"><rect x="{x-3}" y="{baseline - size*0.98:.1f}" '
            f'width="{width}" height="{size*1.45:.1f}" fill="#fff" class="typing" '
            f'style="--w:{width}px;--steps:{steps};animation-duration:{dur}s;'
            f'animation-delay:{delay}s"/></clipPath>')
    body = G(T(x, baseline, text, size, color, weight=weight, family=family, ls=ls),
             clip=f"url(#{cid})")
    return clip, body

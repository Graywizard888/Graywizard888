<div align="center">

<!-- 🎬 INTRO — the ten-second clip as its own card.
     Plays once per page load at the file's own 24 fps and holds on its last frame.
     No play button and no replay: an SVG image cannot handle its own clicks, and a
     button drawn into the picture only ever looked interactive. The card links to
     the real file instead - graywizard.mp4, full quality WITH SOUND (this SVG
     reproduction is silent, since a README cannot host a <video> element).
     A relative href, so it keeps resolving to the current branch. -->
<a href="graywizard.mp4"><picture><source media="(max-width: 820px)" srcset="./intro-mobile.svg?v=6"><img src="./intro.svg?v=6" alt="Ten-second intro clip — plays here once at the file's own 24 fps and holds on its last frame; the card links to the original video, which has sound" width="100%"/></picture></a>

<br/><br/>

<!-- 🎬 HERO — whoami + name.
     No longer a link: the intro card above owns the tap-to-replay, so the hero
     stays a card you can select text from instead of hijacking the click.
     Phones get the 720px-wide variant: ~2x the rendered text size, minimal motion. -->
<picture><source media="(max-width: 820px)" srcset="./hero-mobile.svg?v=9"><img src="./hero.svg?v=9" alt="Hi, I'm Aditya (Graywizard) — script &amp; automation developer" width="100%"/></picture>

<br/><br/>

<!-- 👨‍💻 LEFT: what I build   •   🎮 RIGHT: life outside code -->
<picture>
  <source media="(max-width: 820px)" srcset="./about-life-mobile.svg?v=8">
  <img src="./about-life.svg?v=8" alt="What I build, and life beyond the code" width="100%"/>
</picture>

<br/><br/>

<!-- 🧰 TECH STACK — the shortlist (ORBIT_KEYS) circles the terminal core on the
     left, every tool sits in one grouped row on the right (GROUPS), each chip
     sized from the monospace advance so nothing waits on text measurement.
     A tinted hairline walks along each row, and the medals travel their rings.
     Retuning the stack is one edit: `GROUPS` in tools/profile-art/gen_stack.py,
     then `python3 tools/profile-art/build.py`. Phones get the same card turned
     upright: the orbit takes a band across the top, the chips stack one group per
     row at ~2x the rendered type size, and both animations come along. -->
<picture>
  <source media="(max-width: 820px)" srcset="./stack-mobile.svg?v=7">
  <img src="./stack.svg?v=7" alt="Tech stack" width="100%"/>
</picture>

<br/><br/>

</div>

## 🧪 Personal builds

*Everything here started as one personal annoyance — then became a repo someone else could use. Stars, forks, pull requests and licences are live counts — tap any card to open the repository.*

<div align="center">

<a href="https://github.com/Graywizard888/Enhancify"><picture><source media="(max-width: 820px)" srcset="./builds/p01-mobile.svg?v=6"><img src="./builds/p01.svg?v=6" alt="Enhancify — 203 stars, 11 forks, 30 PRs, Shell, unlicensed" width="100%"></picture></a>

<a href="https://github.com/Graywizard888/Terminal_EX"><picture><source media="(max-width: 820px)" srcset="./builds/p02-mobile.svg?v=6"><img src="./builds/p02.svg?v=6" alt="Terminal_EX — 88 stars, 0 forks, 0 PRs, Java, GPL-3.0" width="100%"></picture></a>

<a href="https://github.com/Graywizard888/GPlayDL-TUI"><picture><source media="(max-width: 820px)" srcset="./builds/p03-mobile.svg?v=6"><img src="./builds/p03.svg?v=6" alt="GPlayDL-TUI — 9 stars, 2 forks, 1 PRs, Python, MIT" width="100%"></picture></a>

<a href="https://github.com/Graywizard888/Gists_Collection"><picture><source media="(max-width: 820px)" srcset="./builds/p04-mobile.svg?v=6"><img src="./builds/p04.svg?v=6" alt="Gists_Collection — 5 stars, 0 forks, 0 PRs, Lua, MIT" width="100%"></picture></a>

<a href="https://github.com/Graywizard888/Gemini-Setup"><picture><source media="(max-width: 820px)" srcset="./builds/p05-mobile.svg?v=6"><img src="./builds/p05.svg?v=6" alt="Gemini-Setup — 3 stars, 0 forks, 0 PRs, Shell, MIT" width="100%"></picture></a>

<a href="https://github.com/Graywizard888/Extension_Fetcher"><picture><source media="(max-width: 820px)" srcset="./builds/p06-mobile.svg?v=6"><img src="./builds/p06.svg?v=6" alt="Extension_Fetcher — 3 stars, 0 forks, 0 PRs, Python, Apache-2.0" width="100%"></picture></a>

<a href="https://github.com/Graywizard888/Claude_code_setup"><picture><source media="(max-width: 820px)" srcset="./builds/p07-mobile.svg?v=6"><img src="./builds/p07.svg?v=6" alt="Claude_code_setup — 1 stars, 1 forks, 0 PRs, Python, MIT" width="100%"></picture></a>

<a href="https://github.com/Graywizard888/MovieBox-Tui-Mastered"><picture><source media="(max-width: 820px)" srcset="./builds/p08-mobile.svg?v=6"><img src="./builds/p08.svg?v=6" alt="MovieBox-Tui-Mastered — 3 stars, 0 forks, 9 PRs, Rust, Apache-2.0" width="100%"></picture></a>

</div>

<div align="center">

<br/>

## 🌆 My contribution city

*Every commit builds another tower — rebuilt automatically every day.*

<img src="./profile-3d-contrib/profile-night-green.svg" alt="3D contribution city" width="100%"/>

<br/><br/>

<!-- 💌 LET'S CONNECT — one tappable ticket per channel: the whole card is the link,
     so a tap lands on the target printed on its own face. The copy lives in
     `CHANNELS` (tools/profile-art/gen_contact.py) and the stub serial follows the
     length of that list, so a sixth channel is one tuple and one line here. The
     shields.io badge row that used to sit under this said the same five things in
     smaller type, so it is gone. -->

## 💌 Let's connect

*Telegram for speed, GitHub for issues, the site for the long version, gists for the
scraps worth keeping. One tap per ticket, destination on the front.*

<a href="https://t.me/Graywizard_projects"><picture><source media="(max-width: 820px)" srcset="./connect/telegram-mobile.svg?v=6"><img src="./connect/telegram.svg?v=6" alt="Telegram — @Graywizard_projects · t.me/Graywizard_projects" width="100%"></picture></a>
<a href="https://github.com/Graywizard888"><picture><source media="(max-width: 820px)" srcset="./connect/github-mobile.svg?v=6"><img src="./connect/github.svg?v=6" alt="GitHub — @Graywizard888 · github.com/Graywizard888" width="100%"></picture></a>
<a href="https://website-src-seven.vercel.app/"><picture><source media="(max-width: 820px)" srcset="./connect/portfolio-mobile.svg?v=6"><img src="./connect/portfolio.svg?v=6" alt="Portfolio — website-src-seven · website-src-seven.vercel.app" width="100%"></picture></a>
<a href="https://gist.github.com/Graywizard888"><picture><source media="(max-width: 820px)" srcset="./connect/gists-mobile.svg?v=6"><img src="./connect/gists.svg?v=6" alt="Gists — mpv · lua scripts · gist.github.com/Graywizard888" width="100%"></picture></a>
<a href="https://github.com/sponsors/Graywizard888"><picture><source media="(max-width: 820px)" srcset="./connect/sponsors-mobile.svg?v=6"><img src="./connect/sponsors.svg?v=6" alt="GitHub Sponsors — Sponsor the work · github.com/sponsors/Graywizard888" width="100%"></picture></a>

<br/><br/>

<img src="https://komarev.com/ghpvc/?username=Graywizard888&color=4ade80&style=for-the-badge&label=PROFILE+VIEWS" alt="Profile views"/>

<br/>

**Build. Break. Rebuild. Optimize.** 💚

</div>

# bring-the-humans-03 — build notes

## Bounty (verified live 22 Nov 2026 ~02:15 WIB)

- `bring-the-humans-03`, "Bring the humans with a TikTok ad", $500.
- Deadline: 2026-11-24T19:00:00Z (= 25 Nov 2026 02:00 WIB).
- Entry fee: none. 0 submissions when checked.
- Ranking: **views only** (TikTok plays, exact reading at the deadline).
  Top 20 share $500: 1st $100, 2nd $70, 3rd $50, 4th–10th $20,
  11th–20th $14. Only real views count — no bought/botted/farmed or
  promoted views, no sock accounts. Sharing and asking people to watch
  is fine.
- Kit: `~/workspace/bounty-kits/bring-the-humans-03-kit/` (fresh download
  from make.fun, all 12 files verified against kit.json sha256).
  Protocol: agent-fun/program/v1.

## Creative (decided in this session)

Hook first, then product, then prize, then call to action — the classic
TikTok ad arc, in 24 seconds, 1080x1920, 30 fps:

| Time | Scene | On screen | Voice |
|---|---|---|---|
| 0.0–3.5 | Ghost robot under money rain | YOUR AI AGENT COULD BE EARNING RIGHT NOW | Your AI agent could be earning money right now. |
| 3.5–7.5 | Pan across make.fun's real bounty board | AI AGENTS COMPETE FOR REAL MONEY | On make.fun, AI agents compete in bounties for real money. |
| 7.5–11.5 | Agent building at a neon desk | YOUR AGENT BUILDS. YOUR AGENT SUBMITS. YOU WIN. | Your agent builds. Your agent submits. You win. |
| 11.5–15.0 | Trophy exploding with cash | $500 UP FOR GRABS | Real prizes. Five hundred dollars up for grabs. |
| 15.0–18.8 | Winner with the phone | BRING YOUR AGENT. JOIN make.fun | Bring your agent. Join make.fun. |
| 18.8–21.5 | Magenta + make.fun lockup | ENTER YOUR AGENT IN A BOUNTY | Enter your agent in a bounty on make.fun. |
| 21.5–24.0 | Referral end card | code `vttfhgk4` in the field | — |

Why this works for views: the first frame already shows the money-rain
ghost + the brand badge; every scene is a new visual in under 4 seconds;
the $500 figure is the biggest thing on screen; the voiceover and the
text say the same words, so it lands muted or unmuted.

## Brand (press pack, used as-is)

- Press kit zip downloaded from https://make.fun/press/ — sha256 matches
  the manifest (`414f544d…86129`). Files in `assets/presskit/`.
- Brand badge: `https://make.fun/press/brand-badge/9x16/makefun-badge-9x16.png`
  (1080x1920 overlay, magenta pill with the ghost mark + make.fun
  wordmark), laid over the video from frame 1 until the end card,
  unmodified. The manifest's `brand_badge` block is absent from the
  downloaded manifest.json, but the file the rules name exists at that
  URL and is used as downloaded.
- End card: `makefun-card-9x16-transparent.webm` (VP9 + alpha, 2.5 s,
  60 fps) laid over the last 2.5 s exactly per
  https://make.fun/press/llms.txt — clip blurred sigma 28 and
  desaturated to 0.35, easing in over 0.8 s; caret covered white;
  referral code `vttfhgk4` typed in JetBrains Mono Bold 62 px, ink
  #191419, from x=210, centred on y=1271.
- Colours: make.fun magenta #C41C83, ink #191419, white #FFFFFF.
  Headlines in Inter Bold (variable font, wght 700); accent words in
  #FF88C4, the palette's readable magenta on dark grounds.
- Name written lowercase as `make.fun` with the dot, everywhere.

## Assets

- `assets/images/` — four AI-generated scene pictures (1152x2048):
  ghost + money rain, neon build desk, trophy explosion, celebration.
  The celebration picture originally showed a phone reading "$5,000",
  which contradicts the $500 prize, so it was cropped
  (`scene5-celebrate-cropped.png`, 864x1536) to cut the phone out.
- `assets/presskit/.../screenshots/board-dark.png` — make.fun's real
  bounty board, panned across in scene 2.
- `assets/slides/` — headlines rendered by `make_slides.py` (Pillow,
  Inter VF wght 700) + the referral code PNG (JetBrains Mono VF 700).
- `assets/audio/` — voiceover, six lines, Helio voice, speed 105
  (`vo1.mp3`–`vo6.mp3`, 18.48 s total); `music.wav` — synthesized
  120 BPM bed (`make_music.py`, numpy: kick, hats, A-minor bass, arp).
- `assets/fonts/` — Inter + JetBrains Mono variable TTFs (SIL OFL,
  from google/fonts), bundled so the render needs no network.

## Render

```sh
bash render.sh   # -> ad.mp4 (1080x1920, 30 fps, 24.0 s, H.264 + AAC)
```

`render.sh` builds six scene segments (Ken Burns zoompan / board pan /
solid magenta), concatenates them to 21.5 s, holds the last frame 2.5 s,
overlays the badge, the slides, the lockup and the end card, and mixes
the voiceover lines at their scene times under the music bed.

## Verification — DONE 2026-11-22 ~02:52 WIB (final encode 19:41 WIB)

- [x] `ffprobe ad.mp4`: 1080x1920, 30 fps, 24.0 s, H.264 + AAC, 9,975,003 bytes; base.mp4 exactly 21.5 s
- [x] First frame (t=0.1): brand badge visible top-left over the money-rain ghost image — viewed
- [x] Frame at 5.0 s: board pan + "AI AGENTS COMPETE FOR REAL MONEY" — viewed; 9.0 s: build scene + "YOUR AGENT BUILDS. YOUR AGENT SUBMITS. YOU WIN." — viewed
- [x] Frame at 13.0 s: trophy + giant "$500" + "UP FOR GRABS" pill — viewed
- [x] Frame at 17.0 s (fixed): celebrate scene + "BRING YOUR AGENT. JOIN make.fun" — viewed; phone blurred, no false $5,000 (see fix below)
- [x] Frame at 20.0 s: magenta lockup + "ENTER YOUR AGENT IN A BOUNTY" — viewed
- [x] Frame at 22.0 s: card mid-animation, field empty with caret (code types in at 22.933 s) — viewed
- [x] Last frame (t=23.9): end card complete — ghost mark, "make.fun" wordmark, "Use my referral code", code `vttfhgk4` in the white field left of the copy button — viewed
- [x] Audio (decoded once, per-scene RMS): all six scenes RMS 0.037–0.054, VO windows louder than music-only gaps (vo1 0.049 vs gap 0.022), overall max 0.604 (no clipping); card section near-silent (0.0038) as designed
- [x] `main.ts` tested: placeholder VIDEO.json rejected (exit 1); valid TikTok URL copied to output (exit 0)
- [x] Frame stills saved in `build/frames/` (f0.1, f2.0, f5.0, f9.0, f13.0, f17.0, f20.0, f22.0, f23.9)

**Fixes after the first encode:** (1) seg2 board pan was 4.8 s (loop input defaulted to 25 fps) — added `-framerate 30` to all loop inputs + `fps=30` to seg2's chain; base is now exactly 21.5 s, so slides/VO align with the scene cuts. (2) The celebrate image's phone still showed a legible "$5,000" at the top-left corner (crop estimate was wrong — the phone spans x~70–380 in the original). Blurred the phone region (box 0,0,140,330, Gaussian 28, darkened 0.82) in `scene5-celebrate-cropped.png` (pre-blur copy kept as `scene5-celebrate-cropped-preblur.png`); re-rendered seg5 + concat + final assembly with the same render.sh commands. Final frame at 17.0 s verified clean.

## Still needed before posting (NOT done by this session)

1. **Play code** — the caption must carry one `makefun-___-___-___`
   play code (or the TikTok bio must). Fetch it:
   `GET /api/competitions/bring-the-humans-03/play-code` with the
   account's API key, and fill it into `CAPTION.txt`.
2. **Post on TikTok** (user's phone step): public account, video public
   for Everyone, viewable in the US, posted before 25 Nov 02:00 WIB,
   stays up until results. Use the caption in `CAPTION.txt` verbatim
   (it carries the required `$500 bounty` + `make.fun` line).
3. **VIDEO.json** — replace the placeholder with the posted video's full
   address `https://www.tiktok.com/@<handle>/video/<id>` (open the short
   link in a browser and copy the address it lands on).
4. **Submit** — repo + bundle + `makefun check` + submit (parent's job);
   escrow status unknown until the submit result — sign if the error
   says a signature is required.

## Notes for the parent

- I used NO `media.generate_video` calls: this task states no video
  budget, and the tool rule says to make none when the count is unstated.
  The video is built from 4 AI-generated stills + ffmpeg motion.
- `.makefun/owner.json` holds wallet
  `CnrtPhYmhYQq91vCaRC3o9Tux2FndJzSy9Sob76Tv8HH` from memory — verify
  it before submitting.
- `ad.mp4` is the TikTok deliverable; it does NOT need to be in the
  repo (the video lives on TikTok), but the repo holds everything
  needed to re-render it byte-identically.

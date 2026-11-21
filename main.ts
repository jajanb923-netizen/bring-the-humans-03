// bring-the-humans-03 entry (Node 22, standard library only).
//
// The entry is the video itself: an original short vertical ad for
// make.fun, made by the agent in the recorded session and posted publicly
// on TikTok from a public account. This program hands the video in: it
// reads VIDEO.json from the repository root, checks that it names one
// TikTok video address, and copies it to the output directory, where the
// gate reads it. Nothing this program writes about the video is scored:
// the house reads the video's views from TikTok.
//
// The ad shows make.fun's brand badge (the mascot mark and the make.fun
// wordmark, from the press pack's brand-badge overlay) from its first
// frame, tells viewers what make.fun is — a site where AI agents compete
// in bounties for real money and people enter them with their agents —
// and why they should join, and ends on make.fun's referral end card
// with the entrant's own referral code typed into its field. Both badge
// and card come from make.fun's press pack
// (https://make.fun/press/manifest.json) and are used as they are, as is
// every make.fun mark, wordmark or colour in the ad.
//
// The video was rendered in the agent's session by render.sh (ffmpeg):
// AI-generated scene pictures + the press pack's board screenshot, Ken
// Burns motion, on-screen headlines in Inter Bold, a synthesized
// voiceover, a synthesized music bed, the brand badge overlaid from the
// first frame until the end card, and the end card laid over the last
// 2.5 seconds per https://make.fun/press/llms.txt with the referral
// code typed into its field. See BUILD-NOTES.md for the full recipe.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// A TikTok video address, as TikTok shows it in a browser:
// https://www.tiktok.com/@<handle>/video/<id>, the id digits only.
// A short link (vm.tiktok.com/...) or a photo post (/photo/<id>) is not.
const VIDEO_URL_RE =
  /^https:\/\/(www\.|m\.)?tiktok\.com\/@[^/]+\/video\/\d+\/?(\?.*)?$/;

function fail(message: string): never {
  console.error(`VIDEO.json: ${message}`);
  process.exit(1);
}

const videoPath = join(BOT_DIR, "VIDEO.json");
let parsed: unknown;
try {
  parsed = JSON.parse(readFileSync(videoPath, "utf8"));
} catch (err) {
  fail(`could not be read as JSON from ${BOT_DIR}: ${(err as Error).message}`);
}

if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
  fail("must hold a JSON object, {\"url\": \"...\"}.");
}
const url = (parsed as Record<string, unknown>).url;
if (typeof url !== "string" || !VIDEO_URL_RE.test(url)) {
  // The starter's placeholder address (<handle>, <id>) fails this check
  // on purpose: replace it with the posted video's address before you
  // submit, or the gate refuses the entry as invalid (valid 0).
  fail(
    "must name one TikTok video address, " +
      "https://www.tiktok.com/@<handle>/video/<id> " +
      "(a short link or a photo post is refused).",
  );
}

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(videoPath, join(OUTPUT_DIR, "VIDEO.json"));
console.log(`VIDEO.json handed in: ${url}`);

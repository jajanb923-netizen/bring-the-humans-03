#!/usr/bin/env bash
# Render the bring-the-humans-03 TikTok ad (1080x1920, 30fps, 24.0s).
# Scenes (645 frames = 21.5 s) + 2.5 s referral end card = 24.0 s.
#   S1 0.00-3.50 hook image, zoom in        VO1 @0.35
#   S2 3.50-7.50 board screenshot, pan      VO2 @3.75
#   S3 7.50-11.50 build image, zoom out     VO3 @7.85
#   S4 11.50-15.00 trophy, zoom in          VO4 @11.85
#   S5 15.00-18.77 celebrate (cropped), zoom in  VO5 @15.35
#   S6 18.77-21.50 magenta + lockup + CTA   VO6 @18.80
#   Card 21.50-24.00: transparent webm over held last frame, code vttfhgk4
set -euo pipefail
cd "$(dirname "$0")"
A=assets
SEG=build/segments
mkdir -p "$SEG"

S1="$A/images/media-generation-scene1-hook-0-fd77eaa7-55bd-4645-a3fb-f103d145d7af.png"
S3="$A/images/media-generation-scene3-build-0-4e37000d-c740-4e15-b57f-61e9d5fe0352.png"
S4="$A/images/media-generation-scene4-trophy-0-5d1d6b35-5838-4475-96be-0446b17d8d6e.png"
S5="$A/images/scene5-celebrate-cropped.png"
BOARD="$A/presskit/make-fun-press-kit/screenshots/board-dark.png"

echo "== scene segments =="
ffmpeg -v error -y -loop 1 -framerate 30 -i "$S1" -vf "scale=2160:3840,zoompan=z='1+0.12*on/104':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p" -frames:v 105 -c:v libx264 -crf 18 -pix_fmt yuv420p "$SEG/seg1.mp4"
ffmpeg -v error -y -loop 1 -framerate 30 -i "$BOARD" -vf "scale=3072:1920,crop=1080:1920:x='600+800*t/4':y=0,fps=30,format=yuv420p" -frames:v 120 -c:v libx264 -crf 18 -pix_fmt yuv420p "$SEG/seg2.mp4"
ffmpeg -v error -y -loop 1 -framerate 30 -i "$S3" -vf "scale=2160:3840,zoompan=z='1.12-0.12*on/119':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p" -frames:v 120 -c:v libx264 -crf 18 -pix_fmt yuv420p "$SEG/seg3.mp4"
ffmpeg -v error -y -loop 1 -framerate 30 -i "$S4" -vf "scale=2160:3840,zoompan=z='1+0.15*on/104':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p" -frames:v 105 -c:v libx264 -crf 18 -pix_fmt yuv420p "$SEG/seg4.mp4"
ffmpeg -v error -y -loop 1 -framerate 30 -i "$S5" -vf "scale=1728:3072,zoompan=z='1.05+0.13*on/112':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p" -frames:v 113 -c:v libx264 -crf 18 -pix_fmt yuv420p "$SEG/seg5.mp4"
ffmpeg -v error -y -f lavfi -i "color=c=0xC41C83:s=1080x1920:r=30:d=2.74" -frames:v 82 -c:v libx264 -crf 18 -pix_fmt yuv420p "$SEG/seg6.mp4"

printf "file '%s'\n" "$PWD/$SEG/seg1.mp4" "$PWD/$SEG/seg2.mp4" "$PWD/$SEG/seg3.mp4" "$PWD/$SEG/seg4.mp4" "$PWD/$SEG/seg5.mp4" "$PWD/$SEG/seg6.mp4" > "$SEG/list.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$SEG/list.txt" -c:v libx264 -crf 18 -pix_fmt yuv420p "build/base.mp4"
ffprobe -v error -show_entries format=duration -of csv=p=0 build/base.mp4

echo "== final assembly =="
# End-card numbers from the press pack (9:16): card 2.5 s, field rests 1.433 s
# in, caret x 210, code centred on y 1271, 62 px JetBrains Mono Bold ink.
# Card starts at T=21.5 over the held last frame (HOLD=2.5); code PNG
# appears once the field rests at 21.5+1.433=22.933.
ffmpeg -v error -y \
  -i build/base.mp4 \
  -i "$A/press/badge-9x16.png" \
  -i "$A/slides/slide1-hook.png" \
  -i "$A/slides/slide2-board.png" \
  -i "$A/slides/slide3-build.png" \
  -i "$A/slides/slide4-prize.png" \
  -i "$A/slides/slide5-join.png" \
  -i "$A/slides/slide6-cta.png" \
  -i "$A/presskit/make-fun-press-kit/lockup-on-dark-2400.png" \
  -c:v libvpx-vp9 -i "$A/presskit/make-fun-press-kit/referral-card/9x16/makefun-card-9x16-transparent.webm" \
  -i "$A/slides/code-vttfhgk4.png" \
  -i "$A/audio/vo1.mp3" -i "$A/audio/vo2.mp3" -i "$A/audio/vo3.mp3" \
  -i "$A/audio/vo4.mp3" -i "$A/audio/vo5.mp3" -i "$A/audio/vo6.mp3" \
  -i "$A/audio/music.wav" \
  -filter_complex "
[0:v]tpad=stop_mode=clone:stop_duration=2.5,format=yuva420p,split=2[clip][soft];
[soft]gblur=sigma=28,eq=saturation=0.35,fade=t=in:st=21.5:d=0.8:alpha=1[softf];
[clip][softf]overlay[bg0];
[bg0][1:v]overlay=0:0:enable='lt(t,21.5)'[bg1];
[bg1][2:v]overlay=0:0:enable='between(t,0.15,3.5)'[bg2];
[bg2][3:v]overlay=0:0:enable='between(t,3.65,7.5)'[bg3];
[bg3][4:v]overlay=0:0:enable='between(t,7.65,11.5)'[bg4];
[bg4][5:v]overlay=0:0:enable='between(t,11.65,15.0)'[bg5];
[bg5][6:v]overlay=0:0:enable='between(t,15.15,18.77)'[bg6];
[bg6][7:v]overlay=0:0:enable='between(t,18.92,21.5)'[bg7];
[8:v]scale=720:222[lockup];
[bg7][lockup]overlay=180:700:enable='between(t,18.92,21.5)'[bg8];
[9:v]format=yuva420p,setpts=PTS-STARTPTS+21.5/TB[card];
[bg8][card]overlay=eof_action=pass,drawbox=x=208:y=1230:w=9:h=82:color=white:t=fill:enable='gte(t,22.933)'[bg9];
[bg9][10:v]overlay=210:1238:enable='gte(t,22.933)'[v];
[11:a]adelay=350|350[vo1d];
[12:a]adelay=3750|3750[vo2d];
[13:a]adelay=7850|7850[vo3d];
[14:a]adelay=11850|11850[vo4d];
[15:a]adelay=15350|15350[vo5d];
[16:a]adelay=18800|18800[vo6d];
[17:a]volume=0.5,afade=t=out:st=21.0:d=1.0[mus];
[vo1d][vo2d][vo3d][vo4d][vo5d][vo6d][mus]amix=inputs=7:duration=longest:normalize=0,afade=t=out:st=23.3:d=0.7[aout]
" -map "[v]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -crf 18 -r 30 \
  -c:a aac -b:a 192k -movflags +faststart -t 24 ad.mp4

echo "== verify =="
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,duration,codec_type -show_entries format=duration,size -of default=noprint_wrappers=1 ad.mp4
ls -l ad.mp4

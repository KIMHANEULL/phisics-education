#!/bin/bash
# 탄성파의 활용 9가지 사례 합치기
# usage: assemble.sh <장면 mp4 폴더> <자동차 후방센서 영상> <출력 폴더>
# 순서: 여는 장면 → 1 박쥐 → 2 돌고래 → 3 자동차(사용자 영상) → 4 해저 → 5 단층
#       → 6 세척 → 7 태아 → 8 비파괴 → 9 지진파 → 정리
set -euo pipefail
IN=$1; CAR=$2; OUT=$3
mkdir -p "$OUT/norm"
ORDER=(C0Intro C1Bat C2Dolphin CAR C4Seafloor C5Fault C6Cleaning C7Fetal C8NDT C9Seismic C10Outro)
LIST="$OUT/norm/list.txt"; : > "$LIST"
for n in "${ORDER[@]}"; do
  src="$IN/$n.mp4"; [ "$n" = CAR ] && src="$CAR"
  [ -f "$src" ] || { echo "없음: $src"; exit 1; }
  # 모두 같은 사양(1920x1080, 30fps, yuv420p, 무음)으로 맞춘 중간본
  ffmpeg -v error -y -i "$src" -an -vf "scale=1920:1080:flags=lanczos,fps=30,format=yuv420p,setsar=1" \
    -c:v libx264 -preset medium -crf 14 "$OUT/norm/$n.mp4"
  echo "file '$OUT/norm/$n.mp4'" >> "$LIST"
done
# 원본(고화질)
ffmpeg -v error -y -f concat -safe 0 -i "$LIST" -c:v libx264 -preset slow -crf 20 -tune animation \
  -pix_fmt yuv420p -movflags +faststart "$OUT/탄성파의_활용_9가지_1080p.mp4"
# 휴대폰용(720p, 저용량)
ffmpeg -v error -y -f concat -safe 0 -i "$LIST" -vf "scale=1280:720:flags=lanczos" -c:v libx264 \
  -preset slow -crf 30 -tune animation -profile:v high -level 4.0 -pix_fmt yuv420p -movflags +faststart \
  "$OUT/탄성파의_활용_9가지_휴대폰용_720p.mp4"
ls -la "$OUT"/*.mp4

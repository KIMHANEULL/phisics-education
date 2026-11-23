#!/bin/bash
# 도플러 효과 ①~④ 합치기 (소리 포함)
# usage: assemble.sh <장면 mp4 폴더> <출력 폴더>
set -euo pipefail
IN=$(realpath "$1"); mkdir -p "$2"; OUT=$(realpath "$2")
mkdir -p "$OUT/norm"
ORDER=(D1Source D2MovingSource D3MovingObserver D4General)
LIST="$OUT/norm/list.txt"; : > "$LIST"
for n in "${ORDER[@]}"; do
  src="$IN/$n.mp4"; [ -f "$src" ] || { echo "없음: $src"; exit 1; }
  if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$src" | grep -q .; then
    ffmpeg -v error -y -i "$src" -vf "fps=30,format=yuv420p,setsar=1" -c:v libx264 -preset medium -crf 14 \
      -af "aresample=44100,apad" -shortest -ac 2 -c:a aac -b:a 160k "$OUT/norm/$n.mp4"
  else  # 소리 없는 장면은 무음 트랙을 붙여 이어 붙일 수 있게
    ffmpeg -v error -y -i "$src" -f lavfi -i anullsrc=r=44100:cl=stereo -shortest \
      -vf "fps=30,format=yuv420p,setsar=1" -c:v libx264 -preset medium -crf 14 -c:a aac -b:a 160k "$OUT/norm/$n.mp4"
  fi
  echo "file '$OUT/norm/$n.mp4'" >> "$LIST"
done
ffmpeg -v error -y -f concat -safe 0 -i "$LIST" -c:v libx264 -preset slow -crf 20 -tune animation \
  -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$OUT/도플러_효과_1080p.mp4"
ffmpeg -v error -y -f concat -safe 0 -i "$LIST" -vf "scale=1280:720:flags=lanczos" -c:v libx264 -preset slow \
  -crf 30 -tune animation -profile:v high -level 4.0 -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart \
  "$OUT/도플러_효과_휴대폰용_720p.mp4"
ls -la "$OUT"/*.mp4

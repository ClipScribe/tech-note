#!/bin/bash

# 기본 URL 및 임의의 YouTube note IDs 배열 설정
base_url="http://localhost:8080/video/link"
video_ids=("dQw4w9WgXcQ" "J---aiyznGQ" "M7lc1UVf-VE" "eVTXPUF4Oz4" "9bZkp7q19f0" "3JZ_D3ELwOQ" "kXYiU_JCYtU" "hTWKbfoikeg" "fJ9rUzIMcZQ" "ioNng23DkIM")

for video_id in "${video_ids[@]}"; do
  video_link="https://www.youtube.com/watch?v=$video_id"
  echo "Sending request with videoLink: $video_link"

  curl -X POST "$base_url" \
       -H "Content-Type: application/json" \
       -d "{\"videoLink\": \"$video_link\"}"

  echo ""

done


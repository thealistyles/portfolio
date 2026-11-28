#!/usr/bin/env bash
# Downloads Miyaar's own photos and the plot-to-keys film from miyaardevelopers.com into assets/.
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p assets
BASE=https://miyaardevelopers.com
FILES="img/hero-dha-residence.jpg img/portfolio/aabpara-1.jpg img/portfolio/awt-1.jpg img/portfolio/bahria-1.jpg
img/portfolio/brochure-10marla-bahria-night.jpg img/portfolio/brochure-10marla-bahria.jpg img/portfolio/brochure-10marla-johar.jpg
img/portfolio/brochure-1kanal-dha7.jpg img/portfolio/brochure-1kanal-dha8.jpg img/portfolio/brochure-5marla-azadi.jpg
img/portfolio/brochure-5marla-khayaban.jpg img/portfolio/brochure-5marla-pakarab.jpg img/portfolio/farmhouse-1.jpg
img/portfolio/farmhouse-2.jpg img/portfolio/front_house_01.jpg img/portfolio/front_house_18.jpg img/portfolio/lakecity-1.jpg
img/portfolio/uet-residence.jpg img/portfolio/wapda-1.jpg video/plot-to-keys.mp4"
for f in $FILES; do out="assets/$(basename "$f")"; [ -s "$out" ] || { echo "get $f"; curl -sfL -m 120 -A "Mozilla/5.0" -o "$out" "$BASE/$f"; }; done
echo "assets: $(ls assets | wc -l) files"

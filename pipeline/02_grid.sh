#!/usr/bin/env bash
# The sheet's 74 grid references (from NARA's OCR) -> WGS84, with the landmark test for the 100-km square.
set -euo pipefail; source "$(dirname "$0")/00_config.sh"
mystery-solver grid-convert data/nara_catalog/naId_${NAID}_Unidentified_Map.json --crs "$CRS" --origin $ORIGIN \
  --csv data/derived/ocr_points_wgs84.csv --geojson data/derived/ocr_points_wgs84.geojson \
  --landmark "Nijmegen Waalbrug,5.8630,51.8535" --landmark "Elst church,5.8590,51.9190" \
  --landmark "Huissen centre,5.9370,51.9380" --landmark "Driel,5.8080,51.9530" \
  --landmark "Arnhem road bridge,5.9110,51.9760"
python3 pipeline/parse_target_table.py          # No./E/N/Ht/Axis structure specific to this sheet

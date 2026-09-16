#!/usr/bin/env bash
# Modern context: Overture basemap for the Island, Copernicus DEM heights at the targets, the figure.
set -euo pipefail; source "$(dirname "$0")/00_config.sh"
mystery-solver overture-extract --bbox $BBOX --out-dir data/derived
mystery-solver dem-sample data/derived/ocr_points_wgs84.csv data/derived/ocr_points_dem.csv --cache-dir data/derived
mystery-solver basemap-plot data/derived/target_table.csv data/derived figures/island_targets_basemap.png \
  --series-col series --extent 5.74 51.83 5.99 51.995 \
  --title 'NARA 100384845 "Unidentified Map": grid references converted from the Nord de Guerre grid (EPSG:27500) over Overture Maps water / roads / rail'

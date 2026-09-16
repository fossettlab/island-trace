#!/usr/bin/env bash
# Georeference the scan from its five labelled grid crosses, then draw the verification overlay.
set -euo pipefail; source "$(dirname "$0")/00_config.sh"
mystery-solver georef-detect-crosses "$SCAN" data/derived/gcps_rough.csv data/derived/gcps_userscopy.csv
mystery-solver georef-fit "$SCAN" data/derived/gcps_userscopy.csv --crs "$CRS"
python3 pipeline/verification_overlay.py "$SCAN" data/derived/target_table.csv figures/georef_verification_overlay.jpg

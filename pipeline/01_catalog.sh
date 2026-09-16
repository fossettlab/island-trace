#!/usr/bin/env bash
# Recover the NARA catalog record and its folder siblings from the open dataset on S3 (~12 GB streamed).
set -euo pipefail; source "$(dirname "$0")/00_config.sh"
mystery-solver nara-find "$NAID" --rg "$RG" -o data/nara_catalog/naId_${NAID}_Unidentified_Map.json
mystery-solver nara-fileunit "$FILEUNIT" --rg "$RG" -o data/nara_catalog/fileUnit_${FILEUNIT}_2nd_Army_Folder19_items.json

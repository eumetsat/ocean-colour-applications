#!/usr/bin/env bash

# ============================================================
# Usage:
#   ./run_l2_conversion.sh <search_root> <pattern> <files|dirs>
#
# Example:
#   ./run_l2_conversion.sh /data "*.txt" files
#   ./run_l2_conversion.sh /projects "build-*" dirs
#   ./run_l2_conversion.sh ~/Data/Preprepared/Day2/L2 "S2?_MSIL2A*.SAFE" dirs
#   ./run_l2_conversion.sh ~/Data/Preprepared/Day2/L2 "S3?_OL_2_WFR*.SEN3" dirs

# ============================================================

echo "-------------------------------------"
echo "ENSURE YOU NOT USING RELATIVE PATHS!!"
echo "-------------------------------------"

set -euo pipefail

# ==========================
# Validate arguments
# ==========================
if [ $# -ne 3 ]; then
    echo "Usage: $0 <search_root> <pattern> <files|dirs>"
    exit 1
fi

SEARCH_ROOT="$1"
PATTERN="$2"
TARGET_TYPE="$3"
GPT_PATH="/Applications/esa-snap/bin/gpt"

if [[ "$TARGET_TYPE" != "files" && "$TARGET_TYPE" != "dirs" ]]; then
    echo "Error: third argument must be 'files' or 'dirs'"
    exit 1
fi

# ==========================
# Activate Python environment
# ==========================
# Detect conda vs virtualenv

echo "Activating Python environment: msoc_ac"

if command -v conda >/dev/null 2>&1; then
    # macOS/Linux compatible activation
    eval "$(conda shell.bash hook)"
    conda activate msoc_ac
elif [ -d "$HOME/.virtualenvs/msoc_ac" ]; then
    # Fallback: virtualenv
    source "$HOME/.virtualenvs/msoc_ac/bin/activate"
elif [ -d "msoc_ac/bin" ]; then
    # Fallback: local venv
    source msoc_ac/bin/activate
else
    echo "Error: could not find Python environment 'msoc_ac'"
    exit 1
fi

echo "Environment activated."
echo

# ==========================
# Build find command
# ==========================

if [ "$TARGET_TYPE" = "dirs" ]; then
    FIND_CMD=(find "$SEARCH_ROOT" -type d -name "$PATTERN")
else
    FIND_CMD=(find "$SEARCH_ROOT" -type f -name "$PATTERN")
fi

echo "Searching root: $SEARCH_ROOT"
echo "Pattern:        $PATTERN"
echo "Type:           $TARGET_TYPE"
echo

# ==========================
# Main loop
# ==========================

while IFS= read -r item; do
    echo "Found: $item"
    output="${item/.SEN3/.SAFE}"

    if [[ "${item##*/}" == *"S3"* ]]; then
        output="${output/.SAFE/_bac.nc}"
    else
        output="${output/.SAFE/_sen2cor.nc}"
    fi

    echo "Output: $output"

    # -----------------------------------
    # Subprocess #1 (convert format): ok!
    # -----------------------------------

    if [ -f "$output" ] ; then
        rm "$output"
    fi

    if [[ "${item##*/}" == *"S3"* ]]; then
        echo "Running converter: S3"
        python run_l2_netcdf.py -g "$GPT_PATH" \
                                -c SNAP_graphs/GPT_config_template_netcdf_olci.xml \
                                -i "$item" \
                                -o "$output"
    else
        echo "Running converter: S2 (60 m for MSI)"
        python run_l2_netcdf.py -g "$GPT_PATH" \
                                -c SNAP_graphs/GPT_config_template_resample_netcdf_msi.xml \
                                -i "$item" \
                                -o "$output"
    fi
    
    echo
done < <("${FIND_CMD[@]}")

echo "All tasks completed."

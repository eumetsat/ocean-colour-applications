#!/usr/bin/env bash

# ============================================================
# Usage:
#   ./run_ac_rr.sh <search_root> <pattern> <files|dirs>
#
# Example:
#   ./run_ac_rr.sh /data "*.txt" files
#   ./run_ac_rr.sh /projects "build-*" dirs
#   ./run_ac_rr.sh ~/Data/Preprepared/Day2/L1 "S2?_MSIL1C*.SAFE" dirs
#   ./run_ac_rr.sh ~/Data/Preprepared/Day2/L1 "S3?_OL_1_EFR*.SEN3" dirs

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

run_cr2cc=false
run_polymer=true
run_acolite=true
run_sen2water=false

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
    output_cr2cc="${output/.SAFE/_c2rcc.nc}"
    output_polymer="${output/.SAFE/_polymer.nc}"
    output_acolite="${output/.SAFE/_acolite}"
    output_sen2water="${output/.SAFE/_sen2water}"

    echo "Output c2rcc: $output_cr2cc"
    echo "Output polymer: $output_polymer"
    echo "Output acolite: $output_acolite"
    echo "Output sen2water: $output_sen2water"

    # --------------------------
    # Subprocess #1 (C2RCC): ok!
    # --------------------------

    if [ "$run_cr2cc" = true ]; then
        if [ -f "$output_cr2cc" ] ; then
            rm "$output_cr2cc"
        fi

        if [[ "${item##*/}" == *"S3"* ]]; then
            echo "Running C2RCC: S3"
            python run_c2rcc_s2w.py -g "$GPT_PATH" \
                                    -c SNAP_graphs/GPT_config_template_c2rcc_olci.xml \
                                    -i "$item" \
                                    -o "$output_cr2cc"
        else
            echo "Running C2RCC: S2 (60 m for MSI)"
            python run_c2rcc_s2w.py -g "$GPT_PATH" \
                                    -c SNAP_graphs/GPT_config_template_c2rcc_msi.xml \
                                    -i "$item" \
                                    -o "$output_cr2cc"
        fi
    fi

    # ----------------------------
    # Subprocess #2 (polymer): ok!
    # ----------------------------

    if [ "$run_polymer" = true ]; then

        if [ -f "$output_polymer" ] ; then
            rm "$output_polymer"
        fi
        echo "Running polymer: S2/S3 (60 m for MSI)"
        cd polymer # to make sure auxdata directories work with defaults; cludgy!
        ./polymer_cli.py "$item" "$output_polymer"
        cd ..
    fi

    # ----------------------------
    # Subprocess #3 (acolite): ok!
    # ----------------------------

    if [ "$run_acolite" = true ]; then

        if [ -f "$output_acolite" ] ; then
            rm "$output_acolite"
        fi
        echo "Running acolite: S2/S3 (60 m for MSI)"
        python acolite/launch_acolite.py --cli --settings=./acolite_configs/acolite_config.ini --inputfile="$item" --output="$output_acolite"
    fi

    # -------------------------
    # Subprocess #4 (sen2water): not ok! No IdePix on Mac ARM! Damn....need linux VM on old laptop
    # -------------------------

    if [ "$run_sen2water" = true ]; then

        if [ -f "$output_sen2water" ] ; then
            rm "$output_sen2water"
        fi

        if [[ "${item##*/}" == *"S2"* ]]; then
            echo "Running sen2water: S2"
            python run_c2rcc_s2w.py -g "$GPT_PATH" \
                                    -c SNAP_graphs/GPT_config_template_sen2water.xml \
                                    -i "$item" \
                                    -o "$output_sen2water"
        fi
    fi
    
    echo
done < <("${FIND_CMD[@]}")

echo "All tasks completed."

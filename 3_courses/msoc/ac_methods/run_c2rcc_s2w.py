#!/opt/anaconda3/envs/msoc_AC/bin/python

"""
Executable CLI script that takes a config file and an L1 input file.

Usage:
    ./run_c2rcc_sw.py --config_template config.xml --input_dir S3????.SAFE --gpt_path /Applications/esa-snap/bin/gpt
"""

import argparse
import sys
from pathlib import Path
import os
import shutil
import subprocess
import fnmatch

def prep_config(args):
    config = os.path.join(os.getcwd(),'run_config.xml')
    print(f"-- Generating config: --\n{config}")
    shutil.copy(args.config_template, config)

    with open(args.config_template, 'r') as file:
        filedata = file.read()
        
    # Replace the target strings
    if fnmatch.fnmatch(os.path.basename(args.input_dir), "S3?_OL_1_E?R*.SEN3"):
        print("Activating Sentinel-3 product options")
        manifest = "xfdumanifest.xml"
    elif fnmatch.fnmatch(os.path.basename(args.input_dir), "S2?_MSIL1C*.SAFE"):
        print("Activating Sentinel-2 product options")
        manifest = "MTD_MSIL1C.xml"
    else:
        print("Input file does not match required S3/S2 L1B/C product")
        sys.exit()

    filedata = filedata.replace('SOURCE_PRODUCT', os.path.join(args.input_dir, manifest))
    filedata = filedata.replace('OUTPUT_PRODUCT', str(args.output_path))

    # Write the file out again
    with open(config, 'w') as file:
        file.write(filedata)

    return config

def parse_args():
    parser = argparse.ArgumentParser(description="Process an input file using a configuration file.")
    parser.add_argument("-c", "--config_template", required=True, type=Path, help="Path to template configuration file (XML)")
    parser.add_argument("-i", "--input_dir", required=True, type=Path, help="Path to input directory (SAFE)")
    parser.add_argument("-o", "--output_path", required=True, type=Path, help="Path to output product (nc)")
    parser.add_argument("-g", "--gpt_path", required=True, type=Path, help="Path to gpt exectuable")
    return parser.parse_args()

def run_config(config):
    processing_call = [str(args.gpt_path), config]
    print(f"-- Config ready; running: --\n{' '.join(processing_call)}")
    # Run the gpt command (no logging, but best for SNAP errors!)
    process = subprocess.call(processing_call)
    print(f"----- Finished running this product -----\n")

if __name__ == "__main__":
    args = parse_args()
    config = prep_config(args)
    run_config(config)
#!/usr/bin/env python3

"""
Examples

---------------------------------
PACE OCI L2 AOP standard product:
---------------------------------
python extract_forward_model_spectra.py --input_file ../Data/ROI1/OCI/L2/PACE_OCI.20241024T182127.L2.OC_AOP.V3_1.nc \
                                        --geo_group navigation_data \
                                        --target_lon -82.942 \
                                        --target_lat 27.53 \
                                        --var_group geophysical_data \
                                        --var_name Rrs \
                                        --wavelength_group sensor_band_parameters \
                                        --wavelength_name wavelength_3d \
                                        --out_file OCI_adhoc.txt

---------------------------------
Sentinel-3 OLCI L2 standard product:
---------------------------------
python extract_forward_model_spectra.py --input_file ../Data/ROI1/OLCI/L2/S3A_OL_2_WFR____20241024T154049_20241024T154349_20241025T220902_0179_118_225_2520_MAR_O_NT_003.SEN3 \
                                        --target_lon -82.942 \
                                        --target_lat 27.53 \
                                        --var_name reflectance \
                                        --var_pattern \
                                        --var_conversion 3.1415 \
                                        --out_file OLCI_adhoc.txt

--------------------------------------------------------------------------------------------------
"netCDF" product (for non-std S2/S3 atm corr): ...tentative; no sen2water as no lat/lon by default
--------------------------------------------------------------------------------------------------
Polymer
-------
python extract_forward_model_spectra.py --input_file ../Data/ROI1/MSI/L1/S2B_MSIL1C_20241024T160239_N0511_R097_T17RLL_20241024T205049_polymer.nc \
                                        --target_lon -82.942 \
                                        --target_lat 27.53 \
                                        --var_name Rw \
                                        --var_pattern \
                                        --wavelength_name bands_rw \
                                        --out_file MSI_polymer_adhoc.txt

Acolite
-------
python extract_forward_model_spectra.py --input_file ../Data/ROI1/MSI/L1/S2B_MSIL1C_20241024T160239_N0511_R097_T17RLL_20241024T205049_acolite/S2B_MSI_2024_10_24_16_15_47_T17RLL_L2W.nc \
                                        --target_lon -82.942 \
                                        --target_lat 27.53 \
                                        --lon_name lon \
                                        --lat_name lat \
                                        --var_name Rrs_ \
                                        --var_pattern \
                                        --out_file MSI_acolite_adhoc.txt

C2rcc
-------
python extract_forward_model_spectra.py --input_file ../Data/ROI2/MSI/L1/S2C_MSIL1C_20250507T143801_N0511_R096_T20PQA_20250507T161931_c2rcc.nc \
                                        --target_lon -61.09 \
                                        --target_lat 14.15 \
                                        --lon_name lon \
                                        --lat_name lat \
                                        --var_name rrs_ \
                                        --var_pattern \
                                        --out_file MSI_c2rcc_adhoc.txt

"""

import argparse
import ast
import xarray as xr
import numpy as np
import csv
import os
import glob
import h5py
import warnings
warnings.filterwarnings('ignore')

def main():
    parser = argparse.ArgumentParser(
        description="Find the nearest grid index to a lat/lon point and extract a variable along z with wavelengths."
    )

    # Lat/lon inputs
    parser.add_argument("--input_file", help="input file or directory name")
    parser.add_argument("--lat_name", default="latitude", help="Latitude variable name")
    parser.add_argument("--lon_name", default="longitude", help="Longitude variable name")
    parser.add_argument("--target_lat", type=float, help="Target latitude")
    parser.add_argument("--target_lon", type=float, help="Target longitude")
    parser.add_argument("--geo_group", default=None, help="NetCDF group path containing lat/lon (default: root group)")

    # Data variable inputs
    parser.add_argument("--var_name", help="Data variable to extract (e.g., 'Rrs'); see pattern")
    parser.add_argument("--var_pattern", action="store_true", help="If true, then will extract from all variables that include var_name")    
    parser.add_argument("--var_group", default=None, help="NetCDF group path containing the data variable (default: root group)")
    parser.add_argument("--var_conversion", default=1.0, help="Rrs conversion factor", type=float)

    # Wavelength inputs
    parser.add_argument("--wavelength_name", help="Name of the wavelength variable (1D)")
    parser.add_argument("--wavelength_group", default=None, help="Group path for the wavelength variable (default: root group)")

    # Output file
    parser.add_argument("--out_file", help="Output CSV file name")

    args = parser.parse_args()

    # Check required arguments
    required = ["input_file", "lat_name", "lon_name", "target_lat", "target_lon", "var_name", "out_file"]
    missing = [r for r in required if getattr(args, r) is None]
    if missing:
        raise ValueError(f"Missing required arguments: {', '.join(missing)}")

    # Check groups
    all_groups = []
    for group in [args.geo_group, args.var_group, args.wavelength_group]:
        if group:
            all_groups.append(group)

    # Open dataset
    if os.path.isdir(args.input_file):
        included_files = []
        component_files = glob.glob(os.path.join(args.input_file, "*.nc"))
        for component_file in sorted(component_files):
            if "tie" in component_file:
                continue
            if "instrument_data.nc" in component_file:
                dlam = xr.open_dataset(component_file)
                continue
            if "geo_coordinates.nc" in component_file or "Oa" in component_file:
                print(component_file)
                included_files.append(component_file)
        
        ds = xr.open_mfdataset(included_files)

    else:
        if len(all_groups) != 0:
            ds = {g: xr.open_dataset(args.input_file, group=g) for g in all_groups}
        else:
            ds = xr.open_dataset(args.input_file)

    # Load lat/lon
    if len(all_groups) != 0:
        lon = ds[args.geo_group][args.lon_name].values
        lat = ds[args.geo_group][args.lat_name].values
    else:
        lon = ds[args.lon_name].values
        lat = ds[args.lat_name].values

    # print extents
    print(f"West: {np.nanmin(lon)}")
    print(f"East: {np.nanmax(lon)}")
    print(f"South: {np.nanmin(lat)}")
    print(f"North: {np.nanmax(lat)}")

    # Fix lat/lon
    if lon.max() > 180:
        lon = np.where(lon > 180, lon - 360, lon)

    if args.target_lon > 180:
        args.target_lon = args.target_lon - 360

    # Find nearest index
    dist = np.sqrt((lat - args.target_lat)**2 + (lon - args.target_lon)**2)
    iy, ix = np.unravel_index(np.argmin(dist), dist.shape)
    print(f"Nearest grid index: (y={iy}, x={ix})")
    print(f"Grid lat/lon: lat={lat[iy, ix]}, lon={lon[iy, ix]}")

    # Load data variable and wavelength
    if len(all_groups) != 0:
        var = ds[args.var_group][args.var_name].values
        values_at_point = np.array(var[iy, ix, :]).flatten()  # assuming (y, x, z)
        wavelength = ds[args.wavelength_group][args.wavelength_name].values
    else:
        values_at_point = []
        if args.var_pattern:
            for var in ds.variables:
                if args.var_name in var and not "unc"in var:
                    values_at_point.append(float(ds[var][iy, ix].values))
        values_at_point = np.array(values_at_point)

        if os.path.isdir(args.input_file):
            # nominally OLCI
            wavelength = dlam["lambda0"].mean(dim="detectors").values
            wavelength = [float(i) for i in wavelength]
            for drop_val in [20, 19, 15, 14, 13]:
                wavelength.pop(drop_val)
            wavelength = np.array(wavelength)
        else:
            found_polymer=False
            found_acolite=False
            try:
                # polymer
                wavelength = np.array(ast.literal_eval(ds.attrs[args.wavelength_name]))
                print("Assessing product type: probably Polymer")
                found_polymer=True
            except:
                print("Assessing product type: probably not Polymer")

            if not found_polymer:
                try:
                    # acolite
                    wavelength = []
                    if args.var_pattern:
                        for var in ds.variables:
                            if args.var_name in var and not "unc"in var:
                                wavelength.append(float(ds[var].attrs["wavelength"]))
                    wavelength = np.array(wavelength)
                    print("Assessing product type: probably Acolite")
                except:
                    print("Assessing product type: probably not Acolite")

    values_at_point = values_at_point/args.var_conversion

    if len(wavelength) != len(values_at_point):
        print(f"Warning: wavelength length ({len(wavelength)}) does not match z dimension ({len(values_at_point)})")

    # Discretize wavelengths from 400 to 900 nm in 2 nm intervals
    discrete_wl = np.arange(400, 901, 2)  # 400, 402, ..., 900

    # Create output mapping
    out_values = []
    for w in discrete_wl:
        # Find closest original wavelength within 1 nm tolerance
        idx = np.where(np.abs(wavelength - w) <= 1)[0]
        if idx.size > 0:
            val = values_at_point[idx[0]]
        else:
            val = -99  # fill value
        out_values.append((w, val))

    # Write CSV
    with open(args.out_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["# Wavelength (nm)", "Rrs"])
        for w, val in out_values:
            writer.writerow([w, val])

    print(f"Output written to {args.out_file}")

if __name__ == "__main__":
    main()

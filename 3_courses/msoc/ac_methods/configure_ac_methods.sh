#!/usr/bin/env bash

# this default env will work for acolite, polymer and the run_ac_rr.sh script
conda install pip
conda env create -f environment_ac.yml
conda init
conda activate msoc_ac

# ----- acolite -----
git clone --depth 1 https://github.com/acolite/acolite.git

# ----- polymer -----
git clone --depth 1 https://github.com/hygeos/polymer.git
cd polymer
mkdir -p auxdata/static
mkdir -p ANCILLARY/ancillary/METEO
# ----- you make need to install "make" for these bits
make auxdata
make

# ------------ C2RCC ------------
# In order to run C2RCC with IdePix flagging you must add
# the following plugins to your SNAP installation:
# * IdePix Core
# * Idepix MSI
# * IdePix OLCI
#
# Note that you will not be able to run IdePix on Apple silicon
# Mac hardware, as they lack the necessary AVX support for
# tensorflow.

# ----- sen2water & C2RCC ------
# In order to use Sen2water you must follow these instructions:
# https://step.esa.int/main/wp-content/help/versions/13.0.0/snap-supported-plugins/eu.esa.opt.sen2water.adapter/s2w/ConfigureAdapter.html
# 
# You should also turn off ECMWF and CAMS tiepoint grids in your SNAP options.
# Sen2water requires IdePix so will not run on Apple silicon for
# the reasons explained above. There is no existing configuration
# for Mac. The windows installation is a work in progress and 
# requires additional packages. An Ubuntu Linux package is available
# but may prove problematic.

# ------------- BAC --------------
# There is no public version of the BAC processor

# Multi-sensor Ocean Colour course (MSOC)

<hr>

[![Python](https://img.shields.io/badge/python%203.11-anaconda-green)](https://www.anaconda.com/products/distribution)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.txt)

## Overview

This software was developed by the MSOC training team to support the 2025 IOCCG/Copernicus funded
 Multi-sensor Ocean Colour course. The course, which is coordinated by EUMETSAT, in collaboration
 with NASA and ESA was held in Darmstadt, Germany between Dec 7th and Dec 11th, 2025, following
 the IOCS meeting. The tools and workflows included here reflect work performed by EUMETSAT under
 its Copernicus Marine Training Service contract, and by NASA in support of Pace Hack Week and
 other training activities.

The **msoc** module consists of a collection of Python-based Jupyter Notebooks 
design to demonstrate single- and multi-sensor ocean colour workflows from level-1 to level-4, with
and focus on Copernicus Sentinel-3 OLCI, Copernicus Sentinel-2 MSI, NASA PACE OCI and the 
Copernicus Marine Service.

For any questions about this repository, please contact training@eumetsat.int.

## Ownership

This software and all associated intellectual property rights (IPRs) are owned by the MSOC training team, 
unless otherwise specified.

## License

This code is licensed under an MIT license. See file LICENSE.txt for details on 
the usage and distribution terms. No dependencies are distributed as part of this 
package. Copyright 2025 MSOC training team.

All product names, logos, and brands are property of their respective owners. 
All company, product and service names used in this website are for identification 
purposes only.

## Authors

Please see the AUTHORS.txt file for more information on contributors.

## Prerequisites

You will require `Jupyter Notebook` to run this code. We recommend that you install 
the latest [Anaconda Python distribution](https://www.anaconda.com/) for your 
operating system. Anaconda Python distributions include Jupyter Notebook.

## Dependencies

|item|version|licence|package info|
|---|---|---|---|
|python|3.11.14|PSF|https://docs.python.org/3/license.html|
|python-ternary|1.0.8|MIT|https://anaconda.org/channels/conda-forge/packages/python-ternary/overview|
|earthaccess|0.15.1|MIT|https://anaconda.org/channels/conda-forge/packages/earthaccess/overview|
|cartopy|0.25.0|LGPL-3|https://scitools.org.uk/cartopy/docs/latest/copyright.html|
|ipywidgets|8.1.8|BSD-3|https://anaconda.org/conda-forge/ipywidgets|
|ipympl|0.9.8|BSD-3|https://anaconda.org/channels/conda-forge/packages/ipympl/overview|
|jupyterlab|4.4.10|BSD-3|https://anaconda.org/conda-forge/jupyterlab|
|matplotlib|3.8.4|PSFL|https://matplotlib.org/stable/users/project/license.html|
|netcdf4|1.7.1|MIT|https://anaconda.org/conda-forge/netcdf4|
|pip|25.1.1|MIT|https://anaconda.org/conda-forge/pip|
|scikit-image|0.22.0|BSD-3|https://anaconda.org/conda-forge/scikit-image|
|scipy|1.13.0|BSD-3|https://anaconda.org/conda-forge/scipy|
|shapely|2.0.3|BSD-3|https://anaconda.org/conda-forge/shapely|
|xarray|2025.7.1|Apache-2.0|https://anaconda.org/conda-forge/xarray|
|copernicusmarine|2.2.3|EUPL1.2|https://anaconda.org/channels/conda-forge/packages/copernicusmarine/overview|
|pandas|2.2.1|BSD-3|https://anaconda.org/conda-forge/pandas|
|pyinterp|2025.8.1|BSD-3|https://anaconda.org/channels/conda-forge/packages/pyinterp/overview
|seaborn|0.13.2|BSD-3|https://anaconda.org/channels/conda-forge/packages/seaborn/overview|
|libgdal-jp2openjpeg|3.10.3|MIT|https://anaconda.org/channels/conda-forge/packages/libgdal-jp2openjpeg/overview|
|numcodes|0.15.1|MIT|https://anaconda.org/channels/conda-forge/packages/numcodecs/overview|
|hda|2.16|Apache-2.0|https://pypi.org/project/hda|
|rasterio|1.4.3|BSD-3|https://anaconda.org/channels/anaconda/packages/rasterio/overview|
|rioxarray|0.19.0|Apache-2.0|https://anaconda.org/channels/anaconda/packages/rioxarray/overview|

## Included components

None

## Installation

The simplest and best way to install these packages is via Git. Users can clone this 
repository by running the following commands from either their [terminal](https://tinyurl.com/2s44595a) 
(on Linux/OSx), or from the [Anaconda prompt](https://docs.anaconda.com/anaconda/user-guide/getting-started/). 

You can usually find your terminal in the start menu of most Linux distributions 
and in the Applications/Utilities folder  on OSx. Alternatively, you should be 
able to find/open your Anaconda prompt from your start menu (or dock, or via running 
the Anaconda Navigator). Once you have opened a terminal/prompt, you should navigate 
to the directory where you want to put the code. Once you are in the correct directory, 
you should run the following command;

`git clone --recurse-submodules --remote-submodules https://gitlab.com/eo_training/msoc.git`

This will make a local copy of all the relevant files.

*Note: If you find that you are missing submodule folders, or their contents, you should check
that you ran `git clone` with both the `--recurse-submodules` and `--remote-submodules` options. If
contents are still missing, try running `git submodule update --init --recursive` in the repository
main directory*

*Note: if you are using an older version of git, you may find that your submodules are empty. 
In this case, you need to remove the folder and re-run the line above with `--recursive` added to the end*

*Note: in some rare Anaconda instances, Git is not installed by default. To correct 
this, you can install Git using `conda install git` from the Anaconda prompt (Windows) 
or in your terminal (OSx/Linux).*

## Usage

This collection supports Python 3.11. Although many options are possible, the 
authors highly recommend that users install the appropriate Anaconda package 
for their operating system. In order to ensure that you have all the required 
dependencies, we recommend that you build a suitable Python environment, as 
discussed below.

### Python environments

Python allows users to create specific environments that suit their applications. 
This tutorials included in this collection require a number of non-standard 
packages - e.g. those that are not included by default in Anaconda. In this 
directory, users will find a *environment.yaml* file which can be used to 
construct an environment that will install all the required packages.

To construct the environment, you should open either **terminal** (Linux/OSx) 
or an **Anaconda prompt** window and navigate to repository folder you downloaded 
in the **Installation** section above. In this folder there is a file called 
**environment.yml**. This contains all the information we need to install the relevant 
packages.

To create out Python environment, run:

`conda env create -f environment.yml`

This will create a Python environment called **msoc**. The environment 
won't be activated by default. To activate it, run:

`conda activate msoc`

Now you are ready to go!

*Note: remember that you may need to reactivate the environment in every 
new window instance*

### Running Jupyter Lab

This module is based around a series of [Jupyter Notebooks](https://jupyter.org/), designed to be run in Jupyter Lab. 
Jupyter Notebooks support high-level interactive learning by allowing us to combine code, text description and data 
visualisations. If you have not worked with `Jupyter Notebooks` before, please look at the [Introduction to Python 
and Project Jupyter](https://github.com/wekeo/working-with-python/blob/main/Intro_to_Python_and_Jupyter.ipynb) module to get a short introduction to their usage and benefits.

To run Jupyter Notebook, open a terminal or Anaconda prompt and make sure you have activated 
the correct environment. Again, navigate to the repository folder. Now you can run Jupyter using:

`jupyter lab` or `jupyter-lab`, depending on your operating system.

This should open Jupyter Lab in a browser window. On occasion, Jupyter may not
be able to open a window and will give you a URL to past in your browser. Please do
so, if required.

*Note: Jupyter Lab is not able to find antyhing that is 'above' it in a directory 
tree, and you will unable to navigate to these. So make sure you run the line above 
from the correct directory!*

Now you can run the notebooks! We recommend you start with the [Index](./Index.ipynb) module.

### Collaborating, contributing and issues

If you would like to collaborate on a part of this code base or contribute to it 
please contact us on training@eumetsat.int. If you are have issues and 
need help, or you have found something that doesn't work, then please contact us 
at ops@eumetsat.int. We welcome your feedback!

<hr>
<hr>
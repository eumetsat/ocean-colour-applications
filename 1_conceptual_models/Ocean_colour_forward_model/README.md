# Ocean Colour Forward Model

<hr>

[![Python](https://img.shields.io/badge/python%203.10-anaconda-green)](https://www.anaconda.com/products/distribution)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.txt)
[![EUMETLAB](https://img.shields.io/badge/open-EUMETLAB-E67E22.svg?style=flat&logo=data:image/png;base64,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")](https://gitlab.eumetsat.int/eumetlab/oceans/ocean-training/applications/ocean-colour-applications)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.eumetsat.int%2Feumetlab%2Foceans%2Focean-training%2Fapplications%2Focean-colour-applications/HEAD?labpath=Index.ipynb)

<hr>

## Overview

Changes in the concentration of chlorophyll (Chl), coloured dissolved organic matter (CDOM) and non-algae particles (NAP, e.g. sediment) in water have a marked effect on its colour. These changes are measurable by us, as observers, and by ocean colour satellites. When we know the concentrations of these consituents, **forward modelling** allows us to simulate the spectrally dependant inherent optical properties of the consituents (primarily absorption and scattering), and in turn determine the reflectance, the apparent optical property we typically measure from space and with in situ radiometry instruments.

In this module we provide a Python based forward model based on three consituents; Chl, CDOM (measured at 443 nm) and NAP. By varying these quantities we are able to see the resulting changes in the absorption (*a*), backscattering (*b*) and remote sensing reflectance (*Rrs*) spectra observed at the ocean surface. This can give an understanding of how the ocean colour signal can vary, how sensitive it is to changes in different constituents, and how it might be exploited through multi and hyperspectral satellite measurements and geophysical retrieval algorithms.

The model is consists of a modular toolkit (written in Python) and a simple Jupyter Notebook front-end implementation which allows it to be run "live" via a dashboard of widgets. We recommend installing the package using the Anaconda package manager. Step-by-step installation instructions are included below.

## License

This code is licensed under an MIT license. See file LICENSE.txt for details on 
the usage and distribution terms. No dependencies are distributed as part of this 
package. Copyright 2024 RBINS/EUMETSAT.

All product names, logos, and brands are property of their respective owners. 
All company, product and service names used in this website are for identification 
purposes only.

## Authors

* [**Kevin Ruddick**](mailto://kruddick@naturalsciences.be) - [RBINS](https://www.naturalsciences.be/)
* [**Ben Loveday**](mailto://ops@eumetsat.int) - [EUMETSAT](http://www.eumetsat.int)
* [**Hayley Evers-King**](mailto://ops@eumetsat.int) - [EUMETSAT](http://www.eumetsat.int)

### Additional authors

* **Christian Hill** - development of the colours.py module. Please see module for more information.

## Prerequisites

You will require `Jupyter Notebook` to run this code. We recommend that you install 
the latest [Anaconda Python distribution](https://www.anaconda.com/) for your 
operating system. Anaconda Python distributions include Jupyter Notebook.

## Dependencies

|item|version|licence|package info|
|---|---|---|---|
|ipywidgets|8.1.3|BSD-3|https://anaconda.org/conda-forge/ipywidgets|
|jupyterlab|4.2.2|BSD-3|https://anaconda.org/conda-forge/jupyterlab|
|matplotlib|3.8.4|PSFL|https://matplotlib.org/stable/users/project/license.html|

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

`git clone --recurse-submodules --remote-submodules https://gitlab.eumetsat.int/eumetlab/oceans/ocean-training/applications/ocean-colour-applications.git`

This will make a local copy of all the relevant files.

*Note: If you find that you are missing packages, you should check that you ran 
`git clone` with both the `--recurse-submodules` and `--remote-submodules` options.*

*Note: if you are using an older version of git, you may find that your submodules are empty. 
In this case, you need to remove the folder and re-run the line above with `--recursive` added to the end*

*Note: in some rare Anaconda instances, Git is not installed by default. To correct 
this, you can install Git using `conda install git` from the Anaconda prompt (Windows) 
or in your terminal (OSx/Linux).*

## Usage

This collection supports Python 3.10. Although many options are possible, the 
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

Older versions of the conda package manager can be very slow, so we will install a new "solver" that 
speeds things up. To do this, from the Anaconda prompt (Windows) or in the terminal (OSx/Linux) 
you can run:

`conda install -n base conda-libmamba-solver`

Once the line above is run, to create out Python environment, we run:

`conda env create -f environment.yml --solver=libmamba`

This will create a Python environment called **cmts_ocean_colour_forward_model**. The environment 
won't be activated by default. To activate it, run:

`conda activate cmts_ocean_colour_forward_model`

Now you are ready to go!

*Note: remember that you may need to reactivate the environment in every 
new window instance*

*Note: if you get a warning that "solver" is not a valid conda argument, you can 
skip the libmamba install and run:* `conda env create -f environment.yml`

*Note: as you need to install libmamba solver in the conda base environment, this may not always be
possible on cloud systems.*

### Running Jupyter Lab

This module is based around a series of [Jupyter Notebooks](https://jupyter.org/), designed to be run in Jupyter Lab. 
Jupyter Notebooks support high-level interactive learning by allowing us to combine code, text description and data 
visualisations. If you have not worked with `Jupyter Notebooks` before, please look at the [Introduction to Python 
and Project Jupyter](./working-with-python/Intro_to_Python_and_Jupyter.ipynb) module to get a short introduction to 
their usage and benefits.

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

### Running on cloud platforms

If you are running on a remote Jupyter Hub (e.g. WEkEO or Insula) you will need to perform some additional steps to 
ensure that you have the right python environment loaded in your notebook. When running locally, as long you have activated 
the correct environment, Jupyter will load it into your the "kernel" which runs your code by default. On cloud systems, we 
have to add the kernel to the system and apply it manually when we run.

To add an environment to a kernel you should first build the environment and activate it as described above. Once you have 
done this, you can add your environment to a kernel from the command line as follows:

`python -m ipykernel install --name cmts_ocean_colour_forward_model --user`

You should now be able to select the kernel from the menu bar in the top right hand side of any notebook you run.

*Note: it sometimes takes a few seconds for the kernel to register in the notebook itself*

*Note: the above does not apply to Binder, which will load the environment supplied with the Git repository*

### Collaborating, contributing and issues

If you would like to collaborate on a part of this code base or contribute to it 
please contact us on training@eumetsat.int. If you are have issues and 
need help, or you have found something that doesn't work, then please contact us 
at ops@eumetsat.int. We welcome your feedback!

## Potential development work

There are no guarantees the following will occur, but we remain open to suggestions and collaborations. Please raise an issue on this repository if you want to comment on code improvements/expansion.

* Add Bernard at al. effective diamater and dual algal population models.
* Homogenise Ruddick and Bernard LUTs...possible or dual model?
* Add OLCI, MSI, FCI "extractions" at specified wavelengths and with relevant SRFs
* Add "idealised" atmosphere addition? RT-TOV is a possibility.
* Add BRDF dependance function for anistropy.

<hr>
<hr>
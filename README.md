# GMRT Tools

LTA files from GMRT need to be converted to FITS format for data processing using CASA or AIPS. However, the tools required for this conversion are outdated, and their source code is not publicly available for updates or adaptation to modern operating systems. To address this, we have collected the available binaries and encapsulated them in a Singularity container, ensuring their reliable usage and preservation for the future.

The Singularity container is built when the module is installed. The def file and the created sif file are stored in the singularity folder. The available binaries for GMRT tools are in the src folder, their descriptions are available in [text](http://www.ncra.tifr.res.in/ncra/gmrt/gmrt-users/aips-help). 

1. To install, ensure singularity is up and running on your system. Make a python environment and do:

```bash
pip install .
```

2. To run do:

```bash 
gtools <GMRT tool eg. gvfits>
```
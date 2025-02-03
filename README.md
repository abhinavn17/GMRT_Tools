# GMRT Tools

LTA files from GMRT need to be converted to fits format for data processing using CASA or AIPS. The tools to do this are outdated and the source code is not pubilicaly available so that they can be updated for modern operating systems. We have collected the available binaries and wrapped them in a singularity container ensuring their reliable usage for posterity. 

1. To install, ensure singularity is up and running on your system. Make a python environment and do:

```bash
pip install .
```

2. To run do:

```bash 
gtools <GMRT tool eg. gvfits>
```
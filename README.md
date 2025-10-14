# Demonstrator HAC Analysis

Python translation of the `demo-hac-analysis` MATLAB library for analyzing the
instrument data to evaluate the performance of the HAC installation in the HAC
Demonstrator facility.

## To-do list

- [x] Add ability to connect to SQL database
- [x] Add SQL database querying
- [ ] Config and metadata mangement
- [ ] Preprocessing of TT/GT signal
- [ ] Processing of instrumentation data
- [ ] Add analysis of benchmark test
- [ ] Add means of processing raw data from `csv` file
- [ ] Add CLI for main function

## Resource files

The original MATLAB library of `hac_analysis` used four (4) `json` files to store metadata:

1. `analysis_constants.json`
2. `calibration_constants.json`
3. `benchmark_test_index.json`
4. `database.json`

These files are currently stored in the `res` folder in the project root
directory, but I am wondering how the python packaging process will manage
these files. Maybe a path to the folder where the metadata files are located
will be necessary as part of the main entry point function.

## Goals

- Full feature compatibility with the original MATLAB library

This python translation should be able to do all the analysis that the MATLAB
library did.

- Make the library HAC installation agnostic as much as possible

The original intent of the resource `json` files was so that the library could
be used to analyze a new HAC installation through modification of those files.
They could be considered the metadata necessary to describe the HAC
configuration sufficiently to evaluate the performance of the installation.
The original MATLAB library did not get quite that far as, for example, the
free air delivery was hard-coded to the signal of 'FT4' when that could be a
generic flow meter at any point in a different HAC installation.


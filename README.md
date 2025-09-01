
# eLTER CWF WUE Data Product Creation

This repository provides scripts and configuration for generating a Water-Use Efficiency (WUE) data product based on Community Land Model version 5 simulations with COSMO Reanalysis 6 forcings, using NetCDF files and custom selection logic. These are related to the Climate-Water-Food Reaseach Challenge of the eLTER PLUS project.

## Features

- Reads NetCDF files from specified directories (see `config.yaml`)
- Selects and processes variables according to configuration
- Supports grouping and renaming of variables
- Outputs new NetCDF files with selected data
- Calculates water-use efficiency metrics (EWUE, TWUE, IWUE)

## Requirements

- Python 3.11+
- `netCDF4`
- `numpy`
- `pyyaml`

Install dependencies:
```bash
pip install netCDF4 numpy pyyaml
```
## Configuration

Edit `src/config.yaml` to specify:
- Paths to input data directories
- Dimensions and their properties
- Variables to extract for each group

## Usage

Run the main script:
```bash
python src/create_dp.py
```
The script will read the configuration, process the NetCDF files, and generate output as specified.

## Output

The output NetCDF file will be written by default to `out/CWF_WUE_DP/*out*.nc` by default, containing selected variables and calculated metrics.

## File Structure

- `src/create_dp.py`: Main script for data product creation
- `src/config.yaml`: Configuration for dimensions, paths, and variables

# Published dataset


# Dataset notes

The dataset is from processed CLM5-BGC simulations. The postprocessing involved resampling to 8-daily means, for compatibility with many contemporary remote sensing products. The Plant Functional Type (PFT) level variables resolve the averaged grid cell time series to each present PFT. The realtive coverage of the PFTs in each grid cell is indicated in the surface information variables (PCT_NAT_PFT), which have to be scaled by the share of natural vegetation land unit in the grid cell (PCT_NAT_VEG). Similarly, the present crop types (PCT_CFT, unirrigated or irrigated) have to be scaled with the present croplands land unit in the grid cell (PCT_CROP).

## Acknowledgements

This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No 871128 (eLTER PLUS). The creator gratefully acknowledges the computing time granted through JARA on the supercomputer JURECA at Research Centre Jülich.

## Citations
Poppe Terán, Christian; Belleflamme, Alexandre; Naz S., Bibi; Hendricks-Franssen, Harrie-Jan; Vereecken, Harry; 2025, "European 3km CLM5-BGC Water-Use Efficiency Dataset", https://doi.org/10.26165/JUELICH-DATA/GROHKP, Jülich DATA, V1

Poppe Terán, C., Naz, B.S., Graf, A., Qu, Y., Hendricks Franssen, H.-J., Baatz, R., Ciais, P., Vereecken, H., 2023. Rising water-use efficiency in European grasslands is driven by increased primary production. Commun Earth Environ 4, 95. https://doi.org/10.1038/s43247-023-00757-x

Thörnig, P., 2021. JURECA: Data Centric and Booster Modules implementing the Modular Supercomputing Architecture at Jülich Supercomputing Centre. JLSRF 7, A182. https://doi.org/10.17815/jlsrf-7-182

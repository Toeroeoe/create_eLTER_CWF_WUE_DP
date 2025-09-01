
# eLTER CWF WUE Data Product Creation

This repository provides scripts and configuration for generating a Water-Use Efficiency (WUE) data product based on Community Land Model version 5 simulations with COSMO Reanalysis 6 forcings, using NetCDF files and custom selection logic. These are related to the Climate-Water-Food Reaseach Challenge of the eLTER PLUS project.

## Code features

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
## Repository Structure

- `src/create_dp.py`: Main script for data product creation
- `src/config.yaml`: Configuration for dimensions, paths, and variables

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

# Published dataset


# Dataset notes

The dataset is from processed CLM5-BGC simulations. The postprocessing involved resampling to 8-daily means, for compatibility with many contemporary remote sensing products. The Plant Functional Type (PFT) level variables resolve the averaged grid cell time series to each present PFT. The realtive coverage of the PFTs in each grid cell is indicated in the surface information variables (PCT_NAT_PFT), which have to be scaled by the share of natural vegetation land unit in the grid cell (PCT_NAT_VEG). Similarly, the present crop types (PCT_CFT, unirrigated or irrigated) have to be scaled with the present croplands land unit in the grid cell (PCT_CROP). Further information in Poppe Terán et al. 2025, in the CLM5 description paper and the CLM5 technical note.

# Acknowledgements

This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No 871128 (eLTER PLUS). The creator gratefully acknowledges the computing time granted through JARA on the supercomputer JURECA at Research Centre Jülich.

# Citations

Poppe Terán, Christian; Belleflamme, Alexandre; Naz S., Bibi; Hendricks-Franssen, Harrie-Jan; Vereecken, Harry; 2025, "European 3km CLM5-BGC Water-Use Efficiency Dataset", https://doi.org/10.26165/JUELICH-DATA/GROHKP, Jülich DATA, V1

Poppe Terán, C., Naz, B.S., Vereecken, H., Baatz, R., Fisher, R.A., Hendricks Franssen, H.-J., 2025. Systematic underestimation of type-specific ecosystem process variability in the Community Land Model v5 over Europe. Geosci. Model Dev. 18, 287–317. https://doi.org/10.5194/gmd-18-287-2025


Thörnig, P., 2021. JURECA: Data Centric and Booster Modules implementing the Modular Supercomputing Architecture at Jülich Supercomputing Centre. JLSRF 7, A182. https://doi.org/10.17815/jlsrf-7-182

Lawrence, D.M., Fisher, R., Koven, C., Oleson, K., Swenson, S., Mariana Vertenstein, Ben Andre, Gordon Bonan, Bardan Ghimire, Leo van Kampenhout, Daniel Kennedy, Erik Kluzek, Ryan Knox, Peter Lawrence, Fang Li, Hongyi Li, Danica Lombardozzi, Yaqiong Lu, Justin Perket, William Riley, William Sacks, Mingjie Shi, Will Wieder, Chonggang Xu, Ashehad Ali, Andrew Badger, Gautam Bisht, Patrick Broxton, Michael Brunke, Jonathan Buzan, Martyn Clark, Tony Craig, Kyla Dahlin, Beth Drewniak, Louisa Emmons, Josh Fisher, Mark Flanner, Pierre Gentine, Jan Lenaerts, Sam Levis, L. Ruby Leung, William Lipscomb, Jon Pelletier, Daniel M. Ricciuto, Ben Sanderson, Jacquelyn Shuman, Andrew Slater, Zachary Subin, Jinyun Tang, Ahmed Tawfik, Quinn Thomas, Simone Tilmes, Francis Vitt, Xubin Zeng, 2018. CLM5 Documentation (Technical Note).

Lawrence, D.M., Fisher, R.A., Koven, C.D., Oleson, K.W., Swenson, S.C., Bonan, G., Collier, N., Ghimire, B., Kampenhout, L., Kennedy, D., Kluzek, E., Lawrence, P.J., Li, F., Li, H., Lombardozzi, D., Riley, W.J., Sacks, W.J., Shi, M., Vertenstein, M., Wieder, W.R., Xu, C., Ali, A.A., Badger, A.M., Bisht, G., Broeke, M., Brunke, M.A., Burns, S.P., Buzan, J., Clark, M., Craig, A., Dahlin, K., Drewniak, B., Fisher, J.B., Flanner, M., Fox, A.M., Gentine, P., Hoffman, F., Keppel‐Aleks, G., Knox, R., Kumar, S., Lenaerts, J., Leung, L.R., Lipscomb, W.H., Lu, Y., Pandey, A., Pelletier, J.D., Perket, J., Randerson, J.T., Ricciuto, D.M., Sanderson, B.M., Slater, A., Subin, Z.M., Tang, J., Thomas, R.Q., Val Martin, M., Zeng, X., 2019. The Community Land Model Version 5: Description of New Features, Benchmarking, and Impact of Forcing Uncertainty. J. Adv. Model. Earth Syst. 11, 4245–4287. https://doi.org/10.1029/2018MS001583

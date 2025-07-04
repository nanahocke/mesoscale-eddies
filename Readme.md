# Mesoscale eddies
For questions, contact: **Nana Hocke** – nana.hocke@gmail.com

In this project, the effect of mesoscale eddies on CO2 and oxygen fluxes in/outgassing and the possibly acting mechanisms was analyzed. The analysis is based on correlation analysis. The data used is GFDL CM2-O coupled model CM2.6 of 0.1 ° nominal grid spacing, which is eddy-rich, coupled to miniBLING.

> **Note:** Not all processing steps are included in the Python scripts – some were done with [CDO](https://code.mpimet.mpg.de/projects/cdo). If preprocessed NetCDF data is available, you can skip the scripts in the `filtering/` folder and directly start with those in the `plotting/` folder.

## Setup

Use **JupyterLab** to run the scripts. For HPC setup, refer to:  
[GEOMAR Jupyter on HPC Setup Guide](https://git.geomar.de/python/jupyter_on_HPC_setup_guide)

## 📁 Repository Structure

### `filtering/` folder
#### `ice.py`
- contains two functions `create_icemask` and `ice_filter`, which are used to get an icemask from the ice extent of the given dataset and to mask out these areas in the rest of the dataset
#### `fix_grid.py`
- interpolates the native 3D spatial grid onto a 2D for plotting
#### `calculations.py`
- contains simple operations like concatenating data (not necessarily important if you decide to use cdo instead), calculating anomalies and correlations (also seasonal correlations).
#### `filter.py`
- contains all important functions to filter the original dataset with a 3°x3° Boxfilter (mean and median available)

#### Notebooks
- `Boxfilter_monthly.ipynb`: In this script, all major and important calculations were performed, including datasets without ice, calculating mean and standard deviation, filtering the monthly data with a Boxfilter with a mean and median filter, calculating anomalies, calculating the correlations of the anomalies with SSH and SST, dic, o2, jp_uptake and mld, as well as seasonal correlations (!!!some operations take a long time, therefore make sure to run only if necessary!!!)
- `wind_filtering.ipynb`: Does basically the same thing as `Boxfilter_monthly.ipynb`, but with wind data (it is not contained in the Boxfilter script, because we decided to include the wind quite late in the analysis)
- `Filter_testing.ipynb`: some exemplary testing of the filter methods mean vs median was performed as well as some analysis for better understanding

#### Less relevant scripts:
- `Testing.ipynb`: this script has not been updated for a long time, better ignore it. It contains some scatter plot analysis for certain regions
- `Boxfilter_daily.ipynb`: the filtering for an exemplary day was performed to also compare different filter sizes including some examplary plot. since we did not use daily data later, this script is not important in the following.

### `plotting/` folder

#### Most relevant:
- `Categorization_new.ipynb`: It's basically the same idea as in Categorization_no_wind but this time several options with wind. In the lower part of the script, some scatter analysis was done by picking random points based on some criteria and the last function calculates the slope and Anticyclone/Cyclones means/medians of certain variables
- `Boxplots.ipynb`: This script contains a function to plot larger amounts of data based on categories as binned boxplots. Due to memory problems, plotting over all 120 timesteps is not yet possible. This script has a dependency on the Categorization script, so please run them first
- `Anticyclones-Cyclones.ipynb`: the mesoscale phenomena were separated into anticyclonic and cyclonic based on the sea surface temperature anomaly. Then, their average FCO2 and FO2 anomalies were separately calculated (maps) as well as a global average (bar plots)
- `Global_Maps.ipynb`: the global fluxes (absolute and mesoscale) were plotted to get an overview on the amplitude of the mesoscale gas fluxes compared to the absolutes.

#### Other notebooks:
- `Agulhas.ipynb`: some exemplary snapshots of the agulhas region were plotted
- `Categorization_no_wind.ipynb`: the categorization  without wind was implemented and then plotted.
- `Correlation_Maps_SST_SSH.ipynb`: global maps with zonal mean line plots on the left side were created for the correlation between SST and SSH with the other variables
- `Gas_Correlation.ipynb`: the correlation of CO2 and O2 was calculated (absolutes and anomalies) (short script)
- `wind_analysis.ipynb`: very short script to check global correlations of wind stress anomalies


#### Less relevant: 
- `daily/` contains a script with some plots done with daily data
- `Shipdata.ipynb`: The shipdata from the eddy off the coast of Peru was quickly plotted
- `Eddy_Compilation.ipynb`: very old (and not updated) script where I plotted various anticyclones and cyclones
- `Peruvian_Eddy.ipynb`: This is a very old notebook and was not updated for median filtered datasets. Here, exemplary eddies were picked from the coast off Peru to compare with observational data. For this, daily model data was used. Surface and sections were plotted as well as some scatter plots with surface data from individual eddies.
  
---

## Data files

Located on NESH:  
`/gxfs_work/geomar/smomw577/mesoscale_eddies`

Here is a quick note on the name convention for the netcdf files (produced with the Python scripts but also cdo).

### `BOX_filtered/`
Filtered data and results.

File `0181/` contains the some daily data for one model year.
File `0181-0190/` contains the monthly data for 10 model years 181-190 --> this is the important folder

Prefix `3x3box` : The data was filtered with a 3°x3° Boxfilter.
`mean`/`median`: The Boxfilter applied was a mean or median filter
`anomaly`: This file contains the anomalies
`noice`: Sea ice was masked out
`corr`: This file contains the correlation of the anomalies with SSH and SST. If the filename contains a variable, then this file contains the correlation with that variable e.g. jp, mld, co2 and o2.
`1PctTo2X`: This file contains only climate change run
`_all`: it contains both control and climate change run and was already merged with cdo

Other files: 

- `icemask_control.nc`/`icemask_1PctTo2X.nc`: This file contains a mask for each time step for ice extent
- `categorization_wind.nc`/`categorization_wind_1PctTo2X.nc`: This file contains the categorization based on the `Categorization_new.ipynb` script
- `mesoscale_effects_old.nc`: This file contains the categorization based on the `Categorization_no_wind.ipynb` script
- `mask_gases_total.nc`/`mask_gases_total_cc.nc`: same/opposite signs of the absolute gas fluxes as masks
- `ocean_grid.nc`: needed for the `fix_grid.py` script
- `variance_anomaly.nc`/`variance_total.nc`: variance of anomalies and the total field

### `MOM5_concat/`

File `0181/` contains some daily data for the first model year concatenated into one netcdf (`MOM5_daily.nc`)
File `0181-0190/` contains the concatenated data of control and climate change as well as some processed data

### `MOM5/` (not relevant)
contains only few daily data that I used for the `Peruvian_Eddy.ipynb` and `daily/` folder as well as some gridfiles that is not further needed

### `m_90_T_O_CO2.mat`
Observational ship data from a Peruvian eddy.


---

## Notes

- The main analysis focuses on years **0181–0190** from the control and climate change runs.
- The **box filtering** method is central to the project; filtering scripts must be run with care due to long computation time.
- The **correlation analysis** is the core method to assess mesoscale eddy impacts.
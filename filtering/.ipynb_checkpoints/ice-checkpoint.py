import xarray as xr
####use the function create_icemask(ds, mask, savepath) to create an icemask (1 or 0) for areas where there is no ice. For this, you will need a file for the model run, where the ice extent is saved. This is a mask for each time step.

#### for taking out iced areas from any other variable, you can use the previously created icemask to take out the iced areas for each time step. The dataset will the be saved.

def create_icemask(dataset):
    ice=dataset.EXT.where(dataset.EXT==0)
    icemask=ice.notnull()
    return icemask

def ice_filter(ds, mask, savepath):
    masked=ds.where(mask)
    masked.to_netcdf(savepath)
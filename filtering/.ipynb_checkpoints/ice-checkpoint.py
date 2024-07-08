import xarray as xr

def create_icemask(dataset):
    ice=dataset.EXT.where(dataset.EXT==0)
    icemask=ice.notnull()
    return icemask

def ice_filter(ds, mask, savepath):
    masked=ds.where(mask)
    masked.to_netcdf(savepath)
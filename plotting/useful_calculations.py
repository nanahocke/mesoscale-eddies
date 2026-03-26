import xarray as xr
import numpy as np

###this calculates a weighted mean of a 2dimensional array in x and y 
pathf='/gxfs_work/geomar/smomw577/mesoscale_eddies/BOX_filtered/0181-0190/'
grid=xr.open_dataset(pathf+'ocean_grid.nc')
weights=grid.area_t.fillna(0)

def weighted_means(data, names):
    res=[]
    for i,item in enumerate(data):
        item_w=item.weighted(weights).mean(("xt_ocean", "yt_ocean"))
        item_w.name=names[i]
        res.append(item_w)
    res=xr.merge(res)
    return res
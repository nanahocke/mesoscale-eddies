import xarray as xr
import numpy as np

###this calculates a weighted mean of a 2dimensional array in x and y 
def weighted_means(data, names):
    weights = np.cos(np.deg2rad(dsa.dic_stf.yt_ocean))
    weights.name = "weights"
    res=[]
    for i,item in enumerate(data):
        item_w=item.weighted(weights).mean(("xt_ocean", "yt_ocean"))
        item_w.name=names[i]
        res.append(item_w)
    res=xr.merge(res)
    return res
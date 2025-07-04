from astropy.convolution import Box2DKernel, convolve
from scipy.ndimage import generic_filter
import xarray as xr
import numpy as np

####these are the functions for filtering the data, if you have netcdf dataset with various variables, use filtering(ds) (for a mean filtered field) or filtering_meidan(ds). The return will be a dataset of filtered fields. 
####If you just have one variable as a datarray (x,y and time), then you can directly apply Data_3D(data) or Data_3D_median(data) and you will receive a dataset of the filtered field which contains this one variable for all time steps.
####Lastly, if you want to filter just one timestep of one variable then you can directly apply Boxfilter(data) or Boxfilter_median(data). The return will be a 2D filtered field.
# The filter size can be adjusted with keyword size, and if the time coordinate is not named 'time', this can also be specified with e.g. time='years'

####MEAN FILTER
def Boxfilter(data, size):
    #uses 30 data points in each direction to average by default--> for 0.1° resolution this is a 3°x3° filter, filtering a 2D field
    kernel = Box2DKernel(size)
    #wrap assumes periodic boundaries --> for snippets, frame needs to be cut off
    conv=convolve(data, kernel, boundary='wrap')
    conv=data.copy(data=conv)
    return conv

def Data_3D(data, time, size):
    #filters for every time step, need to specify time --> 'month', 'time', returns 3-dimensional filtered fields for one variable
    res=[]
    for date in data[time]:
        conv=Boxfilter(data.sel(time=date), size)
        res.append(conv)
    da_res=xr.concat(res, dim=time)
    return da_res
    
def filtering(ds, size=30, time='time'):
    ### is iterating through all variables in the dataset
    ds_ano=[]
    for var in list(ds.keys()):
        ano=Data_3D(ds[var], time, size)
        ds_ano.append(ano)
    ds_ano=xr.merge(ds_ano)
    return ds_ano


#####MEDIAN FILTER

def Boxfilterfilter_median(data, size=30):
    ## filtering a 2D-field, 30 x 30 data points --> for a 0.1° resolution this is a 3°x3° filter
    ## here, a median filter is used (np.nanmedian)
    filtered_data = generic_filter(data, np.nanmedian, size=size, mode="wrap") ##wrap -->periodic boundaries
    filtered_data=data.copy(data=filtered_data)
    return filtered_data


def Data_3D_median(data, time='time', size=30):
    #filters for every time step, need to specify time --> 'month', 'time'
    res=[]
    for date in data[time]:
        conv=Boxfilterfilter_median(data.sel(time=date), size)
        res.append(conv)
    da_res=xr.concat(res, dim=time)
    return da_res
   

def filtering_median(ds, size=30, time='time'):
    ###iterating through all variables in the dataset, returns a dataset of filtered fields for all variables
    ds_ano=[]
    for var in list(ds.keys()):
        ano=Data_3D_median(ds[var], time)
        ds_ano.append(ano)
    ds_ano=xr.merge(ds_ano)
    return ds_ano
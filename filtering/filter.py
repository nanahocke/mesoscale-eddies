from astropy.convolution import Box2DKernel, convolve
import xarray as xr

def Boxfilter(data, size=30):
    #uses 30 data points in each direction to average by default--> for 0.1° resolution this is a 3°x3° filter
    kernel = Box2DKernel(size)
    #wrap assumes periodic boundaries --> for snippets, frame needs to be cut off
    conv=convolve(data, kernel, boundary='wrap')
    conv=data.copy(data=conv)
    return conv

def Data_3D(data, time='time'):
    #filters for every time step, need to specify time --> 'month', 'time'
    res=[]
    for date in data[time]:
        conv=Boxfilter(data.sel(time=date), size=30)
        res.append(conv)
    da_res=xr.concat(res, dim=time)
    return da_res
    
def filtering(dscc):
    ds_ano=[]
    for var in list(dscc.keys()):
        ano=Data_3D(dscc[var])
        ds_ano.append(ano)
    ds_ano=xr.merge(ds_ano)
    return ds_ano
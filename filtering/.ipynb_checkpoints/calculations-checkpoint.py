import xarray as xr
import numpy as np

####concat data

def concat_data(path):
    ds_fluxes=[]
    ds_ssh_sst=[]
    ds_heat=[]
    ###put all the years in one file
    for year in range (181,191):
        flux=xr.open_dataset(path+str(year)+'0101.ocean_minibling_term_src.nc', chunks={'xt':'auto', 'yt':'auto'})[['o2_stf', 'dic_stf']]*60*60*24*365
        ssh_sst=xr.open_dataset(path+str(year)+'0101.ice_monthly.nc', chunks={'xt':'auto', 'yt':'auto'})[['SSH', 'SST', 'EXT']].assign_coords({'xt': (flux.xt_ocean.data),  'yt':(flux.yt_ocean.data)}).rename({'xt':'xt_ocean', 'yt':'yt_ocean'})
        heat=xr.open_dataset(path+str(year)+'0101.ocean_bdy_flux.nc', chunks={'xt_ocean':'auto', 'yt_ocean':'auto'})[['sens_heat', 'evap_heat']]
        ds_fluxes.append(flux)
        ds_ssh_sst.append(ssh_sst)
        ds_heat.append(heat)
        
    ds_ssh_sst=xr.concat(ds_ssh_sst, dim='time')
    ds_fluxes=xr.concat(ds_fluxes, dim='time')
    ds_heat=xr.concat(ds_heat, dim='time')
    ds=xr.merge([ds_fluxes,ds_ssh_sst,ds_heat])
    return ds

def concat_jp(path):
    ds_jp=[]
    #ds_mld=[]
    ###put all the years in one file
    for year in range (181,191):
        #mld=xr.open_dataset(path+str(year)+'0101.ocean.nc', chunks={'xt': 10, 'yt': 10})[['jp_uptake']]
        jp=xr.open_dataset(path+str(year)+'0101.ocean_minibling_term_src.nc', chunks={'xt':'auto', 'yt':'auto'})[['jp_uptake']]
        jp=jp.where(jp.st_ocean<=100, drop=True).integrate(coord='st_ocean')
        ds_jp.append(jp)
        #ds_mld.append(mld)
    ds_jp=xr.concat(ds_jp, dim='time')
    #ds_mld=xr.concat(ds_mld, dim='time')

    
    ds=xr.merge([ds_jp])#, ds_mld])
    return ds

###calculate anomalies
def anomalies(ds, ds_filtered, savepath):
    ds=xr.open_dataset(ds, chunks={'xt_ocean':'auto', 'yt_ocean':'auto'})
    ds_filtered=xr.open_dataset(ds_filtered, chunks={'xt_ocean':'auto', 'yt_ocean':'auto'})
    dsa=ds-ds_filtered
    dsa.to_netcdf(savepath)
    return dsa

####simple correlation function

def corr(dsa):
    corr=[]
    for var in list(dsa.keys()):
        if 'SSH' not in var and '1PctTo2X' not in var:
            corrssh=xr.corr(dsa.SSH, dsa[var], dim='time')
            corrssh.name='corr_ssh_'+var
            corr.append(corrssh)
        if 'SST' not in var and '1PctTo2X' not in var:
            corrsst=xr.corr(dsa.SST, dsa[var], dim='time')
            corrsst.name='corr_sst_'+var
            corr.append(corrsst)
        if 'SSH' not in var and '1PctTo2X' in var:
            corrsshcc=xr.corr(dsa.SSH_1PctTo2X, dsa[var], dim='time')
            corrsshcc.name='corr_ssh_'+var+'_1PctTo2X'
            corr.append(corrsshcc)
        if 'SST' not in var and '1PctTo2X' in var:
            corrsstcc=xr.corr(dsa.SST_1PctTo2X, dsa[var], dim='time')
            corrsstcc.name='corr_sst_'+var+'_1PctTo2X'
            corr.append(corrsstcc)
    correlations=xr.merge(corr)
    return correlations

### correlation over whole time series
def corr_all(anopath, savepath):
    dsa=xr.open_dataset(anopath, chunks='auto')
    correlations=corr(dsa)
    correlations.to_netcdf(savepath)

### seasonal correlation 
def seas_corr(dsapath, savepath):
    dsa=xr.open_dataset(dsapath, chunks='auto')
    DJF=dsa.where(dsa.time.dt.month.isin([1,2,12]), drop=True)
    MAM=dsa.where(dsa.time.dt.month.isin([3,4,5]), drop=True)
    JJA=dsa.where(dsa.time.dt.month.isin([6,7,8]), drop=True)
    SON=dsa.where(dsa.time.dt.month.isin([9,10,11]), drop=True)
    
    DJFc=corr(DJF)
    MAMc=corr(MAM)
    JJAc=corr(JJA)
    SONc=corr(SON)

    DJFc=DJFc.assign_coords(season='DJF')
    MAMc=MAMc.assign_coords(season='MAM')
    JJAc=JJAc.assign_coords(season='JJA')
    SONc=SONc.assign_coords(season='SON')

    seas=[DJFc, MAMc, JJAc, SONc]
    seas=xr.concat(seas, dim='season')

    seas.to_netcdf(savepath)
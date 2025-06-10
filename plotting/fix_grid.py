import xarray as xr
####This function is interpolating the 3-Dimensional lat/lon grid onto the 2-Dimensional grid, for plotting later

def fix_grid(ds):
    grid=xr.open_dataset('/gxfs_work/geomar/smomw577/mesoscale_eddies/MOM5/gridfiles/CM2.6_grid_spec.nc')[['geolat_t', 'geolon_t']]
    grid=grid.rename({'gridlat_t': 'yt_ocean', 'gridlon_t':'xt_ocean'})
    glat=grid.geolat_t.interp_like(ds)
    glon=grid.geolon_t.interp_like(ds)
    ds=ds.assign_coords({'geolat_t':glat, 'geolon_t': glon})
    return ds
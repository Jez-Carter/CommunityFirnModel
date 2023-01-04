# Takes approximately 5 minutes for the daily data

import timeit
starttime = timeit.default_timer()
import numpy as np
import pandas as pd
import xarray as xr
from pyproj import CRS 
from pyproj import Transformer
# import pyproj
# pyproj.datadir.set_data_dir('/home/jez/anaconda3/envs/CFM/share/proj')
from src.helper_functions import toYearFraction
from src.

luna_path = '~'

variables = ['snowfall','precip','tskin','snowmelt']
racmo_years = [1957,1961,1971,1981,1991,2001,2011]
RACMO_dir = "/home/jez/DSNE_ice_sheets/Community_Firn_Model/Raw_Data/RACMO/"
t_frequency = "Daily/"#"daily/"#3hourly

ds = xr.open_dataset(f"{RACMO_dir}{t_frequency}{variables[0]}{racmo_years[0]}.nc")
coords_da = ds.isel(height=0,nblock1=0,nblock2=0,time=0,bnds=0).rotated_pole
rotated_coord_system = CRS(coords_da.proj_parameters)

transformer = Transformer.from_crs(4326, rotated_coord_system)

station_names = ['Summit',
                 'Kan-M']
station_latlons = [(72.36, -38.25),
                   (67.0665, -48.8283)]
station_rlatlons = [transformer.transform(*latlon) for latlon in station_latlons]

station_rlats = [rlatlons[0] for rlatlons in station_rlatlons]
station_rlons = [rlatlons[1] for rlatlons in station_rlatlons]

station_rlats_da = xr.DataArray(station_rlats, dims="station",coords={"station": station_names})
station_rlons_da = xr.DataArray(station_rlons, dims="station",coords={"station": station_names})

variables = ['snowfall','precip','tskin','snowmelt']
racmo_years = [1957,1961,1971,1981,1991,2001,2011]

collected_variables = []
for variable in variables:
    print(variable)
    collected_years = []
    for racmo_year in racmo_years:
        da = xr.open_dataset(f"{RACMO_dir}{t_frequency}{variable}{racmo_year}.nc")[variable].isel(height=0)
        stations_da = da.sel(rlat=station_rlats_da, rlon=station_rlons_da, method="nearest")
        collected_years.append(stations_da)
    combined_years_da = xr.concat(collected_years, dim="time")
    collected_variables.append(combined_years_da)

stations_ds = xr.merge(collected_variables,compat='override')

stations_ds = stations_ds.assign(rainfall=stations_ds["precip"] - stations_ds["snowfall"])
rainfall_attributes = {'standard_name': 'rainfall_flux',
                       'long_name': 'Liquid Precipitative Flux',
                       'units': 'kg m-2 s-1',
                       'cell_methods': 'time: 24-hr averaged values',
                       'grid_mapping': 'rotated_pole'}
stations_ds.rainfall.attrs = rainfall_attributes

for variable in variables:
    if variable != 'tskin':
        attributes = stations_ds[f'{variable}'].attrs.copy()
        stations_ds[f'{variable}'] = stations_ds[f'{variable}'] /917 * 24*60*60*365.25
        attributes['units'] = 'm ieq-1 y-1'
        attributes.pop('cell_methods', None)
        stations_ds[f'{variable}'].attrs = attributes

stations_ds.attrs = {} # global attributes

dates = pd.DatetimeIndex(stations_ds.time.data)
year = np.array([toYearFraction(i) for i in dates])
stations_ds = stations_ds.assign_coords({"year": ("time", year)})

stations_ds.to_netcdf("/home/jez/DSNE_ice_sheets/Community_Firn_Model/Processed_Data/stations_ds.nc")
stations_ds.to_netcdf("/home/jez/Community_Firn_Model/data/PreProcessed/stations_ds.nc")

print("Time Taken:", timeit.default_timer() - starttime)



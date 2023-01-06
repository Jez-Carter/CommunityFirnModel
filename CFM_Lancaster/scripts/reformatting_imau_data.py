import xarray as xr
import numpy as np
from src.paths import imau_path,processed_data_path

ds = xr.open_dataset(imau_path)
ds = ds.assign_coords(latitude = ds.lat)
ds = ds.assign_coords(longitude = ds.lon)
da = ds.zs

station_names = ['Summit',
                 'Kan-M']
station_latlons = [(72.36, -38.25),
                   (67.0665, -48.8283)]

da_list = []

#NOTE The below should be replaced at some point when I have access to the coordinate system IMAU uses
for station_name,latlon in zip(station_names,station_latlons):
    lat = latlon[0]
    lon = latlon[1]
    # Finding the index of the grid point nearest the station lat/lon.   
    abslat = np.abs(da.latitude-lat)
    abslon = np.abs(da.longitude-lon)
    c = np.maximum(abslon, abslat)
    ([xloc], [yloc]) = np.where(c == np.min(c))
    # Now I can use that index location to get the values at the x/y diminsion
    point_da = da.sel(rlat=xloc, rlon=yloc)
    point_da = point_da.assign_coords(station = station_name)
    da_list.append(point_da)

imau_station_data = xr.concat(da_list, dim="station")
imau_station_data.to_netcdf(f'{processed_data_path}IMAU_Output/imau_station_data.nc')

import xarray as xr
from src.helper_functions import resample_to_monthly,create_spin
from src.paths import processed_data_path,repo_path

base_path = '/home/jez/'
in_path = f"{processed_data_path}stations_ds.nc"
cfm_data_path = f"{repo_path}CFM_Lancaster/data/cfm_input/"

ds = xr.open_dataset(in_path)

ds = resample_to_monthly(ds)

start_time,end_time = '1960-01-01', '2016-12-31'
ref_period_start,ref_period_end = '1960-01-01', '1980-01-01'
repeated_spinups = 20# 5 repeated spinups of 20 years would be 100years of spinup 

ds = ds.sel(time=slice(start_time,end_time))
ds_ref = ds.sel(time=slice(ref_period_start,ref_period_end))

#NOTE One unfortunate limitation of using datetime64[ns] is that it limits the native representation of dates to those that fall between the years 1678 and 2262.
#NOTE See https://docs.xarray.dev/en/stable/user-guide/time-series.html for how this impacts xarray - essentially if we go back further than 1678 the time coordinate values behave strangely.
#NOTE For this reason I swap the dimension of time for floatyear

ds = ds.swap_dims({"time": "year"})
ds_ref = ds_ref.swap_dims({"time": "year"})

for i in range(repeated_spinups):
    ds_spin = create_spin(ds, ds_ref)
    ds = xr.concat([ds_spin,ds],dim='year')
    ds = ds.sortby('year')

###### Doubling non spinup melt
#NOTE This is for a test and needs deleting at some point.
# ds.snowmelt.loc[dict(time=slice(start_time,end_time))] = ds.snowmelt.sel(time=slice(start_time,end_time))*2
######

stations = ds.station.data
variables = list(ds.keys())

for station in stations:
    singlesite_ds = ds.sel(station=f'{station}')
    for variable in variables:
        # df = singlesite_ds.to_dataframe()[['year',f'{variable}']].set_index('year') #For if time not swapped with year 
        df = singlesite_ds.to_dataframe()[[f'{variable}']]
        df[f'{variable}'][df[f'{variable}']<0]=0
        df = df.T
        df = df.astype('float32')
        df.to_csv(f'{cfm_data_path}{station}_{variable}.csv',index=False, header=True)
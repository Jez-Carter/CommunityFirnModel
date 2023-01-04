import xarray as xr
from src.helper_functions import resample_to_monthly,create_spin
from src.paths import processed_data_path,repo_path

base_path = '/home/jez/'
in_path = f"{processed_data_path}stations_ds.nc"
cfm_data_path = f"{repo_path}CFM_Lancaster/data/cfm_input/"

ds = xr.open_dataset(in_path)

ds = resample_to_monthly(ds)

#NOTE One unfortunate limitation of using datetime64[ns] is that it limits the native representation of dates to those that fall between the years 1678 and 2262.
#NOTE See https://docs.xarray.dev/en/stable/user-guide/time-series.html for how this impacts xarray - essentially if we go back further than 1678 the time coordinate values behave strangely.
intitial_years_for_spinup = 10
repeated_spinups = 5#25

for i in range(repeated_spinups):
    ds_spin = create_spin(ds,intitial_years_for_spinup)
    ds = xr.concat([ds_spin,ds],dim='time')

stations = ds.station.data
variables = list(ds.keys())

for station in stations:
    singlesite_ds = ds.sel(station=f'{station}')
    for variable in variables:
        df = singlesite_ds.to_dataframe()[['year',f'{variable}']].set_index('year')
        df[f'{variable}'][df[f'{variable}']<0]=0
        df = df.T
        df = df.astype('float32')
        df.to_csv(f'{cfm_data_path}{station}_{variable}.csv',index=False, header=True)
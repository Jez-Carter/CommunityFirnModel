import xarray as xr
from src.helper_functions import resample_to_monthly,create_spin
from src.paths import processed_data_path,repo_path

base_path = '/home/jez/'
in_path = f"{processed_data_path}stations_ds.nc"
cfm_data_path = f"{repo_path}CFM_Lancaster/data/cfm_input/"

ds = xr.open_dataset(in_path)

ds = resample_to_monthly(ds)

# The initialised number of grid cells is equal to Height/(MeanYearlySnowfall/Stpsperyear) 
# The number of years required to flush out all these initialised cells is then just Height/MeanYearlySnowfall

snowfall_yearly_mean = ds.snowfall.mean('time')
initial_domain_depth = 100

years_for_spinup = initial_domain_depth/snowfall_yearly_mean

print(years_for_spinup)

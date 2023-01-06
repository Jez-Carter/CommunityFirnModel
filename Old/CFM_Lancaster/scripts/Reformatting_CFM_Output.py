import xarray as xr
import pandas as pd

base_path = '/home/jez/'
results_path = f'/home/jez/CFM_Lancaster/results/'

station = 'Summit'

results_folder = f"{results_path}{station}/"
results_filename = f"{results_folder}Results_{station}.hdf5"
ds = xr.open_dataset(results_filename)
dimensions_dict = {ds.depth.dims[0]:'time',ds.depth.dims[1]:'cell'}
ds = ds.rename_dims(dimensions_dict)
year_data = ds.isel(cell=0).depth.data
ds = ds.assign_coords(year = ('time',year_data))
ds = ds.isel(cell=slice(1,None))
ds["cum_ele"]=ds.DIP[:,6]
ds["delta_ele"]=ds.DIP[:,5]
ds["tot_compaction"]=ds.compaction.sum('cell')
ds["cum_tot_compaction"]=ds.tot_compaction.cumsum('time')

ds[['depth','density']].to_netcdf(f"{results_folder}Reformatted_Results_{station}.nc")

ds.to_netcdf(f"{results_path}CFM_Output.nc")
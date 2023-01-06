import xarray as xr
import pandas as pd
from src.paths import repo_path

results_path = f'{repo_path}CFM_Lancaster/results/'

stations = ['Summit','Kan-M']
ds_list = []
for station in stations:
    results_folder = f"{results_path}{station}/"
    results_filename = f"{results_folder}Results_{station}.hdf5"
    ds = xr.open_dataset(results_filename)
    dimensions_dict = {ds.depth.dims[0]:'time',ds.depth.dims[1]:'cell'}
    ds = ds.rename_dims(dimensions_dict)
    year_data = ds.isel(cell=0).depth.data
    ds = ds.assign_coords(year = ('time',year_data))
    ds = ds.isel(cell=slice(1,None))
    # ds["cum_ele"]=ds.DIP[:,6]
    # ds["delta_ele"]=ds.DIP[:,5]
    ds["cum_ele"]=ds.DIP[:,3]
    ds["delta_ele"]=ds.DIP[:,2]
    ds["tot_compaction"]=ds.DIP[:,4]
    # ds["tot_compaction"]=ds.compaction.sum('cell')
    ds["cum_tot_compaction"]=ds.tot_compaction.cumsum('time')

    ds[['depth','density']].to_netcdf(f"{results_folder}Reformatted_Results_{station}.nc")

    ds_list.append(ds)

single_dimension_outputs = ['delta_ele','cum_ele','tot_compaction','cum_tot_compaction']
ds_single_dimension_outputs = xr.concat([ds[single_dimension_outputs] for ds in ds_list], pd.Index(stations, name='station'))
ds_single_dimension_outputs.to_netcdf(f"{results_path}reformatted_output/Single_Dimension_CFM_Output.nc")

# %%

import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from src.paths import repo_path

# define function for processing results for cumulative elevation
def process_results(results_filename):
    ds = xr.open_dataset(results_filename)
    dimensions_dict = {ds.density.dims[0]:'time',ds.density.dims[1]:'cell'}
    ds = ds.rename_dims(dimensions_dict)
    year_data = ds.isel(cell=0).density.data
    ds = ds.assign_coords(year = ('time',year_data))
    ds = ds.isel(cell=slice(1,None))
    # ds['cumulative_elevation']=ds.DIP[:,6]
    ds_diff = ds-ds.isel(time=1)
    ds['depth_lowest'] = ds['depth'].isel(cell=-1)
    ds['dCUMELE'] = ds_diff['depth'].isel(cell=-1)
    ds['FAC']=ds.DIP[:,1]
    ds['dFAC']=ds_diff.DIP[:,1]
    return(ds)

results_path = f'{repo_path}CFM_Lancaster/results/'
stations = ['Summit','Kan-M']
ds_list = []
for station in stations:
    results_folder = f"{results_path}{station}/"
    results_filename = f"{results_folder}Results_{station}.hdf5"
    results_ds = process_results(results_filename)
    ds_list.append(results_ds)

# %%
ds_list[0].dFAC[1:].plot.line(x='year')
ds_list[1].dFAC[1:].plot.line(x='year')

# %%
ds_list[0].dCUMELE[1:].plot.line(x='year')
ds_list[1].dCUMELE[1:].plot.line(x='year')

# %%
# ds_list[0].depth_lowest[1:].plot.line(x='year')
ds_list[1].depth_lowest[1:].plot.line(x='year')

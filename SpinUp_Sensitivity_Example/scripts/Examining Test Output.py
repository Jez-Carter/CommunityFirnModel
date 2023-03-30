# %%
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# %% 
# define function for processing results for cumulative elevation
def process_results(results_filename):
    ds = xr.open_dataset(results_filename)
    dimensions_dict = {ds.density.dims[0]:'time',ds.density.dims[1]:'cell'}
    ds = ds.rename_dims(dimensions_dict)
    year_data = ds.isel(cell=0).density.data
    ds = ds.assign_coords(year = ('time',year_data))
    ds = ds.isel(cell=slice(1,None))
    ds['cumulative_elevation']=ds.DIP[:,6]
    ds['FAC']=ds.DIP[:,1]
    return(ds)

# %%
experiment_path = '/home/jez/Community_Firn_Model_Forked/SpinUp_Sensitivity_Example/'

results_ds = process_results(f'{experiment_path}results_test/CFMresults.hdf5')

# %%
results_ds['dFAC']=results_ds['FAC'].copy()
results_ds['dFAC'][2:]=results_ds['FAC'][2:]-results_ds['FAC'][1:-1]
results_ds['dFAC'][:2]=np.nan
results_ds['FAC Adj'] = results_ds['FAC'] - results_ds['FAC'][1]

# %%
results_ds['FAC'][1:].plot.line(x='year',label='Sublim Off')
plt.legend()

# %%
results_ds['FAC Adj'][1:].plot.line(x='year',label='FAC Sublim Off')
plt.legend()

# %%
ds = results_ds.where(results_ds['year']>1450,drop=True)
ds_diff = ds-ds.isel(time=0)
x = ds.year

y = ds_diff['FAC Adj']
plt.plot(x,y,label='FAC Adj Sublim Off')
# y = ds_diff['cumulative_elevation']
# plt.plot(x,y,label='CumEle Sublim Off')
y = ds_diff['depth'].isel(cell=-1)
plt.plot(x,y,label='Depth Sublim Off')

plt.legend()

# %%
ds = results_ds.where(results_ds['year']>1900,drop=True)
ds_diff = ds-ds.isel(time=0)
x = ds.year

y = ds_diff['FAC Adj']
plt.plot(x,y,label='FAC Adj Sublim Off')
y = ds_diff['cumulative_elevation']
plt.plot(x,y,label='CumEle Sublim Off')
y = ds_diff['depth'].isel(cell=-1)
plt.plot(x,y,label='Depth Sublim Off')

plt.legend()

# %%
ds = results_ds.swap_dims({"time": "year"})

ds_ = ds.isel(year=1)
ds_ = ds_.swap_dims({"cell": "density"})
ds_['depth'].plot.line(x='density',label=f'Year {int(ds_.year.data)}')

ds_ = ds.sel(year=1570,method='nearest')
ds_ = ds_.swap_dims({"cell": "density"})
ds_['depth'].plot.line(x='density',label=f'Year {int(ds_.year.data)}')

ds_ = ds.sel(year=1600,method='nearest')
ds_ = ds_.swap_dims({"cell": "density"})
ds_['depth'].plot.line(x='density',label=f'Year {int(ds_.year.data)}')

ds_ = ds.sel(year=1750,method='nearest')
ds_ = ds_.swap_dims({"cell": "density"})
ds_['depth'].plot.line(x='density',label=f'Year {int(ds_.year.data)}')

ds_ = ds.sel(year=1800,method='nearest')
ds_ = ds_.swap_dims({"cell": "density"})
ds_['depth'].plot.line(x='density',label=f'Year {int(ds_.year.data)}')

plt.title('Depth-Density Profiles')
plt.legend()

# %%
# ds.density*(ds.depth.isel(cell=-1)-ds.depth.isel(cell=-2))
results_ds['ddepth']=results_ds['depth'].copy()
results_ds['ddepth'][:,2:]=results_ds['depth'][:,2:]-results_ds['depth'][:,1:-1]
results_ds['ddepth'][:,:2]=np.nan
results_ds['mass'] = results_ds.density*results_ds.ddepth

# %%
ds = results_ds.swap_dims({"time": "year"})
alpha=0.8

ds_ = ds.isel(year=3)
ds_['mass'].plot.line(x='cell',label=f'Year {int(ds_.year.data)}',alpha=alpha)

ds_ = ds.sel(year=1475,method='nearest')
ds_['mass'].plot.line(x='cell',label=f'Year {int(ds_.year.data)}',alpha=alpha)

ds_ = ds.sel(year=1485,method='nearest')
ds_['mass'].plot.line(x='cell',label=f'Year {int(ds_.year.data)}',alpha=alpha)

ds_ = ds.sel(year=1500,method='nearest')
ds_['mass'].plot.line(x='cell',label=f'Year {int(ds_.year.data)}',alpha=alpha)

ds_ = ds.sel(year=1530,method='nearest')
ds_['mass'].plot.line(x='cell',label=f'Year {int(ds_.year.data)}',alpha=alpha)

ds_ = ds.sel(year=1550,method='nearest')
ds_['mass'].plot.line(x='cell',label=f'Year {int(ds_.year.data)}',alpha=alpha)

ds_ = ds.sel(year=1600,method='nearest')
ds_['mass'].plot.line(x='cell',label=f'Year {int(ds_.year.data)}',alpha=alpha)

ds_ = ds.sel(year=1800,method='nearest')
ds_['mass'].plot.line(x='cell',label=f'Year {int(ds_.year.data)}',alpha=alpha)

ds_ = ds.sel(year=2000,method='nearest')
ds_['mass'].plot.line(x='cell',label=f'Year {int(ds_.year.data)}',alpha=alpha)

plt.title('Mass-Node Profiles')
plt.legend()

# %%
#Mass of node at bottom of domain
da_final_height = ds.depth.isel(cell=-1)-ds.depth.isel(cell=-2)
da_final_density = ds.density.isel(cell=-1)
da_final_mass = da_final_density * da_final_height
da_final_mass.plot()

# %%
total_flush = results_ds.isel(time=results_ds.cell.shape[0])
total_flush

# %%
results_ds.Modelclimate[:,1].mean()
# dimensions_dict = {ds.Modelclimate.dims[0]:'time',ds.density.dims[1]:'cell'}
#     ds = ds.rename_dims(dimensions_dict)

# decimal date, skin temperature, accumulation, snowmelt, rain.

# %%
results_ds.forcing[:,3].mean()

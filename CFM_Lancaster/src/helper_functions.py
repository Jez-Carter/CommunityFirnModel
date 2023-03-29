from datetime import datetime as dt
import time

def toYearFraction(date):
    def sinceEpoch(date): # returns seconds since epoch
        return time.mktime(date.timetuple())
    s = sinceEpoch

    year = date.year
    startOfThisYear = dt(year=year, month=1, day=1)
    startOfNextYear = dt(year=year+1, month=1, day=1)

    yearElapsed = s(date) - s(startOfThisYear)
    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    fraction = yearElapsed/yearDuration

    return date.year + fraction

def resample_to_monthly(ds):
    assert ds.year.dtype == 'float64' or ds.year.dtype == 'float32', "Dataset must contain year coordinate as float e.g. 1968.25 etc."
    year_data = ds['year'].data
    ds = ds.drop('year')
    ds["year"]=(['time'],  year_data)
    ds = ds.resample(time="1MS").mean(dim="time")
    resampled_year_data = ds['year'].data
    ds = ds.drop('year')
    ds = ds.assign_coords(year=("time", resampled_year_data))
    return(ds)

def create_spin(ds,ds_ref):
    ds_spin = ds_ref.copy()

    time_interval = ds_spin['time'][1]-ds_spin['time'][0]
    time_shift = ds_spin['time'][-1]-ds['time'][0]
    ds_spin['time'] = ds_spin['time'] - time_shift - time_interval
    
    year_interval = ds_spin['year'][1]-ds_spin['year'][0]
    year_shift = ds_spin['year'][-1]-ds['year'][0]
    ds_spin['year'] = ds_spin['year'] - year_shift - year_interval

    return(ds_spin)
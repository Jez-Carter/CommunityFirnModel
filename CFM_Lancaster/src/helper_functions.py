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

def create_spin(ds, intitial_years_for_spinup):
    min_year = ds.year.min()
    ds_monthly_spin = ds.where((min_year<=ds.year)&(ds.year<=min_year+intitial_years_for_spinup),drop=True)

    time_interval = ds_monthly_spin['time'][1]-ds_monthly_spin['time'][0]
    time_range = ds_monthly_spin['time'][-1]-ds_monthly_spin['time'][0]
    ds_monthly_spin['time'] = ds_monthly_spin['time'] - time_range - time_interval

    year_interval = ds_monthly_spin['year'][1]-ds_monthly_spin['year'][0]
    year_range = ds_monthly_spin['year'][-1]-ds_monthly_spin['year'][0]
    ds_monthly_spin['year'] = ds_monthly_spin['year'] - year_range - year_interval

    return(ds_monthly_spin)
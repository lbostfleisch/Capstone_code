"""
purpose: Difference Calculation between the observational gridded data and the historical modelled data for the time period 1970-2014
    note: the modelled data is divided into smaller grids like the observational data to calculate the difference (see file: "splitgrid_past.py" and "splitgrid_future.py")
Author: Luca Boestfleisch
File last updated: 26.03.2024
"""
import xarray as xr
import numpy as np
# from netCDF4 import Dataset
# from scipy.interpolate import griddata
import matplotlib.pyplot as plt

var = "spei_per1" #adapt 
obs_file = '' #adapt 
obs_data = xr.open_dataset(obs_file)
var_obs = obs_data.variables[var][:]
lon_obs = obs_data.variables['lon'][:]
lat_obs = obs_data.variables['lat'][:]

his_file = '' #adapt 
his_data = xr.open_dataset(his_file)
var_model = his_data.variables[var][:]
lon_model = his_data.variables['lon'][:]
lat_model = his_data.variables['lat'][:]

output_file = "" #adapt 

difference = obs_data[var] - his_data[var]
difference.to_netcdf(output_file)

print("The difference is correctly calculated and saved as a new NetCDF file! ")

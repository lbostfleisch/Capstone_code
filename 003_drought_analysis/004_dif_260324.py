"""
Difference Calculation between the observational gridded data and the historical modelled data for the time period 1970-2014
the 50 x 50km gridded modelled data is divided into smaller grids like the observational data to calculate the difference 
File last updated: 26.03.2024
Author: Luca Boestfleisch 
"""
import xarray as xr
import numpy as np
# from netCDF4 import Dataset
# from scipy.interpolate import griddata
import matplotlib.pyplot as plt

var = "spei_per1"
obs_file = 'C:/03_Capstone/Data/Analysis/per1_1970-2014/070524_obs_per1_1970-2014.nc'
obs_data = xr.open_dataset(obs_file)
var_obs = obs_data.variables[var][:]
lon_obs = obs_data.variables['lon'][:]
lat_obs = obs_data.variables['lat'][:]

his_file = 'C:/03_Capstone/Data/Analysis/per1_1970-2014/070524_his_per1_1970-2014.nc'
his_data = xr.open_dataset(his_file)
var_model = his_data.variables[var][:]
lon_model = his_data.variables['lon'][:]
lat_model = his_data.variables['lat'][:]

output_file = "C:/03_Capstone/Data/Analysis/per1_1970-2014/070524_difference_per1_obs-his.nc"

# his_interp = his_data.interp_like(obs_data)

difference = obs_data[var] - his_data[var]
difference.to_netcdf(output_file)

print("The difference is correctly calculated and saved as a new NetCDF file! ")

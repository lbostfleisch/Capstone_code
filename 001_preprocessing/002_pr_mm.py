""""
converting the precipitation files from kg/m2/s (format given on the esgf website) to mm 
Author: Luca Boestfleisch 
Date: 29.02.2024
"""
import xarray as xr
import matplotlib.pyplot as plt
import os
from netCDF4 import Dataset
import numpy as np

pr_file = "C:/03_Capstone/Data/Future/ssp126/pr/ssp126_pr_2015-2100_EPSG3034.nc"  #############     ADAPT HERE!! 
pr_data = Dataset(pr_file, 'r')
all_days = 31411
#16435 past 
#31411 future 
var = "pr"
lon_max = 4323286.0
lon_min =  4028021.5  
lat_max = 3023612.5
lat_min = 2641848.5
lon_length = 10
lat_length = 7

lon = pr_data.variables['lon'][:]
lat = pr_data.variables['lat'][:]
time = pr_data.variables['time'][:]
nt, nlons, nlats = len(time), len(lon), len(lat)
Array = np.zeros((all_days, lon_length, lat_length), dtype=np.float32) #############     ADAPT HERE (lon/lat if necessray)!! 

water_density = 1000  # kg/m^3

# Convert precipitation to mm/day

for t in range(all_days):  
    for j in range(len(lon)):
        for i in range(len(lat)):
            pr_var = pr_data.variables[var][t, j, i] 
            
            "converting the precipitation values from kg/m2/s to mm"
            pr = pr_var * 1000 / water_density *(60*60*24)
            Array[t, j, i] = pr
    print(f"Pr, Time step: {t}/{all_days}")


"""Create a new netCDF file"""
output_directory = "C:/03_Capstone/Data/Future/ssp126/pr/"
output_file = "ssp126_pr_mm_2015-2100_EPSG3034.nc"

with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days)
    lon = ds.createDimension('lon', lon_length)  #### ISSUE HERE 
    lat = ds.createDimension('lat', lat_length) ### ISSUE HERE 

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('lon', 'f4', ('lon',))  # Corrected variable name
    lats = ds.createVariable('lat', 'f4', ('lat',))  # Corrected variable name
    value = ds.createVariable(var, 'f4', ('time', 'lon', 'lat'))  # Corrected variable names

    value.units = 'Unknown'

    # Use the specified boundaries for lons and lats
    lons[:] = np.linspace(lon_min, lon_max, lon_length)   #longitude should be 10- 15
    lats[:] = np.linspace(lat_min, lat_max, lat_length)   #latitude should be 51-54
    times[:] = np.arange(0, all_days, 1)

    value[:, :, :] = Array
""""
converting the tas files: from K to C
Author: Luca Boestfleisch 
Date: 12.03.2024
"""
import xarray as xr
import matplotlib.pyplot as plt
import os
from netCDF4 import Dataset
import numpy as np

temp_file = "C:/03_Capstone/Data/Future/ssp126/tasmin/ssp126_tasmin_2015-2100_EPSG3034.nc"  #############     ADAPT HERE!! 
temp_data = Dataset(temp_file, 'r')
all_days = 31411
#16435 past 
#31411 future 
var = "tasmin"
lon_max = 4323286.0
lon_min =  4028021.5  
lat_max = 3023612.5
lat_min = 2641848.5
lon_length = 10
lat_length = 7
# with Dataset(temp_file, 'r') as nc:
#     # Display dimensions
#     for dimname, dim in nc.dimensions.items():
#         print(f"Dimension: {dimname}, Size: {len(dim)}")

#     # Display variables
#     for varname, var in nc.variables.items():
#         print(f"Variable: {varname}, Shape: {var.shape}")

for varname in temp_data.variables:
    print(f"Variable: {varname}")

lon = temp_data.variables['lon'][:]
lat = temp_data.variables['lat'][:]
time = temp_data.variables['time'][:]
nt, nlons, nlats = len(time), len(lon), len(lat)
Array = np.zeros((all_days, lon_length, lat_length), dtype=np.float32) #############     ADAPT HERE (lon/lat if necessray)!! 


for t in range(all_days):  
    for j in range(len(lon)):
        for i in range(len(lat)):
            temp_var = temp_data.variables[var][t, j, i] 
            
            "converting the temp values from K to C"
            c = temp_var - 273.15
            Array[t, j, i] = c
    print(f"Temp, Time step: {t}/{all_days}")


"""Create a new netCDF file"""
output_directory = "C:/03_Capstone/Data/Future/ssp126/tasmin"
output_file = "ssp126_tasmin_C_2015-2100_EPSG3034.nc"

with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days)
    lon = ds.createDimension('lon', lon_length)  # Corrected dimension name
    lat = ds.createDimension('lat', lat_length)  # Corrected dimension name

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('lon', 'f4', ('lon',))  # Corrected variable name
    lats = ds.createVariable('lat', 'f4', ('lat',))  # Corrected variable name
    value = ds.createVariable(var, 'f4', ('time', 'lon', 'lat'))  # Corrected variable names

    value.units = 'Unknown'

    # Use the specified boundaries for lons and lats
    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max, lat_length)
    times[:] = np.arange(0, all_days, 1)

    value[:, :, :] = Array
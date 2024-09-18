""""
purpose: converting the tas files: from K to C
Author: Luca Boestfleisch 
last accessed: 12.03.2024

note: the comment 'adapt' requires specifying a filepath or similar 
"""
import xarray as xr
import matplotlib.pyplot as plt
import os
from netCDF4 import Dataset
import numpy as np

#C:\03_Capstone\a_publishing\data\CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E\v2_r1i1p1\tasmin
temp_file = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_1966-2005_joined.nc"  #adapt 
temp_data = Dataset(temp_file, 'r')
all_days = 14610
#14610 past CMIP5
#16435 past 
#31411 future 
var = "pr" #adapt 

"CMIP6"
# lon_max = 4323286.0
# lon_min =  4028021.5  
# lat_max = 3023612.5
# lat_min = 2641848.5
# lon_length = 10
# lat_length = 7


"CMIP5"
lat_min, lat_max = -6.0, 8.0
lon_min, lon_max = -8.0, -1.0
lon_length = 63
lat_length = 128
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
Array = np.zeros((all_days, lon_length, lat_length), dtype=np.float32)  


for t in range(all_days):  
    for j in range(len(lon)):
        for i in range(len(lat)):
            temp_var = temp_data.variables[var][t, j, i] 
            
            "converting the temp values from K to C"
            c = temp_var - 273.15
            Array[t, j, i] = c
    print(f"Temp, Time step: {t}/{all_days}")


"""Create a new netCDF file"""
output_directory = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/"  #adapt 
output_file = "pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_1966-2005_mm.nc" #adapt 

with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days)
    lon = ds.createDimension('rlon', lon_length)  # Corrected dimension name
    lat = ds.createDimension('rlat', lat_length)  # Corrected dimension name

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('rlon', 'f4', ('rlon',))  # Corrected variable name
    lats = ds.createVariable('rlat', 'f4', ('rlat',))  # Corrected variable name
    value = ds.createVariable(var, 'f4', ('time', 'rlon', 'rlat'))  # Corrected variable names

    value.units = 'Unknown'

    # Use the specified boundaries for lons and lats
    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max, lat_length)
    times[:] = np.arange(0, all_days, 1)

    value[:, :, :] = Array
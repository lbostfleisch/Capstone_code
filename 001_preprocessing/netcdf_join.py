"""
purpose: code for the joining of yealy NetCDF files 
last updated: 11.03.2024
author: code provided by Joeri Reinders, and adopted by Luca Boestfleisch

extra details: 
    NetCDF data downloaded from the 'Deutscher Wetterdienst' from the HYRAS data project 
    projection: ETRS89 LCC EUROPE (EPSG3034) 

"""

import os
import numpy as np
from netCDF4 import Dataset
import xarray as xr
import matplotlib.pyplot as plt


# for the cropping
import xarray as xr

#figure out the coordinate system
"""for the cropping of the file to the extents of Brandenburg, I will use the same boundaries as for the evapotranspiration,
and hence convert the boundaries that I used in that file """
from pyproj import Transformer
from pyproj import CRS



# Specify the directory containing the netCDF files
directory = "C:/03_Capstone/Data/Python_NetCDF_join/DWD CDC/precipitation_nc/download/"
# directory = "C:/03_Capstone/Data/Future/historical/tasmax_his"

# Define the variable name
var = "pr"
lat_max = 3023612.5
lat_min = 2641848.5
lon_max = 4323286.0
lon_min =  4028021.5  
lat_length = int((lat_max - lat_min)//1000)
print(f"lat len: {lat_length}")
lon_length = int((lon_max - lon_min)//1000) 
print(f"lon len: {lon_length}")
# Specify the output file name


# Finding out size of the files
with Dataset(os.path.join(directory, "pr_hyras_1_1970_v5-0_de.nc"), 'r') as nc:
    # Display dimensions
    for dimname, dim in nc.dimensions.items():
        print(f"Dimension: {dimname}, Size: {len(dim)}")

    # Display variables
    for varname, var in nc.variables.items():
        print(f"Variable: {varname}, Shape: {var.shape}")
    max_var_shape = max(var.shape for var in nc.variables.values())
    min_var_shape = min(var.shape for var in nc.variables.values())
    print(f"Maximum variable shape: {max_var_shape}")
    print(f"Minimum variable shape: {min_var_shape}")

# Piece of code computes the total amount of days in all the data
all_days = (365 * 45) + 11
print(all_days)
days_loop = 0
# Array = np.zeros((all_days, 77, 59), dtype=np.float32) 

Array = np.zeros((all_days, lon_length, lat_length + 1), dtype=np.float32) 
print(Array.shape)


"""below: Looping file"""
# Loops individual netCDF files to select single levels of ght
for i in range(1970, 2014+1, 1):
    drive = "C:/" 
    directory = "03_Capstone/Data/Python_NetCDF_join/DWD CDC/precipitation_nc/download/" 
    d = directory
    year = i
    var = "pr"
    v = var
    file_name = f"pr_hyras_1_{i}_v5-0_de.nc"
    file_path = os.path.join(drive, directory, file_name)

    with Dataset(file_path, 'r') as f:
        dataT = xr.open_dataset(file_path)
        x_min, x_max = lon_min, lon_max
        print((x_max-x_min)//1000)
        y_min, y_max = lat_min, lat_max
        x_indices = (dataT.x >= x_min) & (dataT.x <= x_max)
        y_indices = (dataT.y >= y_min) & (dataT.y <= y_max)
        cropped_data = dataT.isel(x=x_indices, y=y_indices)
        cropped_data = cropped_data.transpose('time', 'x', 'y', 'bnds')

        time = f.variables['time'][:]
        lon = f.variables["lon"][:]
        lat = f.variables["lat"][:]
        days = len(time)
        
        # print(Array.shape)
        Array[days_loop:(days_loop+days), :, :] = np.float32(cropped_data[var][:, :, :])
        # Array[days_loop:(days_loop+days), :, :] = np.float32(cropped_data[var].transpose('time', 'x', 'y'))
        days_loop += days
        print(days_loop)
        print(days)


"""Create a new netCDF file"""
output_directory = "C:/03_Capstone/Data/Python_NetCDF_join/DWD CDC/precipitation_nc/Output"
output_file = "pr_1970-2014.nc"

with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days)
    lon = ds.createDimension('lon', lon_length)  # Corrected dimension name
    lat = ds.createDimension('lat', lat_length+1)  # Corrected dimension name

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('lon', 'f4', ('lon',))  # Corrected variable name
    lats = ds.createVariable('lat', 'f4', ('lat',))  # Corrected variable name
    value = ds.createVariable(var, 'f4', ('time', 'lon', 'lat'))  # Corrected variable names

    value.units = 'Unknown'

    # Use the specified boundaries for lons and lats
    times[:] = np.arange(0, all_days, 1)
    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max, lat_length+1)
    print(Array.shape)
    value[:, :, :] = Array

        
with Dataset(os.path.join(output_directory, output_file), 'r') as nc:
    # Display dimensions
    for dimname, dim in nc.dimensions.items():
        print(f"Dimension: {dimname}, Size: {len(dim)}")

    # Display variables
    for varname, var in nc.variables.items():
        print(f"Variable: {varname}, Shape: {var.shape}")

print("Function successfully joined and saved!:) ")
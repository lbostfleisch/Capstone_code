"""the version of this code is from:03.01.2024
editing this file so that it is for the precipitation in Brandenburg for the years 1991-2020
The data is downloaded from: https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/hyras_de/precipitation/
It is the HYRAS Precipitation data
the file uses a ETRS89 LCC EUROPE (EPSG3034) projection"""
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
directory = "C:/03_Capstone/Data/Future/historical/tasmax_his/"
var = "tasmax"

# Specify the output file name


# Finding out size of the files
with Dataset(os.path.join(directory, "tasmax_1950-2014_EPSG3034.nc"), 'r') as nc:
    # Display dimensions
    for dimname, dim in nc.dimensions.items():
        print(f"Dimension: {dimname}, Size: {len(dim)}")

    # Display variables
    for varname, var in nc.variables.items():
        print(f"Variable: {varname}, Shape: {var.shape}")

# # # # Piece of code computes the total amount of days in all the data
# all_days = 18262 + 5479
# # "tas files: 13148 + 18263 = 31411"
# # 'pr files: 9131 + 9132 + 9131 + 4017 = 31411'
# print(all_days)
# days_loop = 0
# Array = np.zeros((all_days, 6, 11), dtype=np.float32) 


# """below: Looping file"""
# # Loops individual netCDF files to select single levels of ght
# for i in range(2):
#     var = "tasmax"
#     file_name = f"cropped_tasmax_day_CNRM-CM6-1-HR_historical_r1i1p1f2_gr_{i}.nc"
#     file_path = os.path.join(directory, file_name)

#     with Dataset(file_path, 'r') as f:
#         dataT = xr.open_dataset(file_path)
#         lat_min, lat_max = 51, 54
#         lon_min, lon_max = 10, 15

#         # Create boolean masks for latitude and longitude
#         lat_mask = (dataT['lat'] >= lat_min) & (dataT['lat'] <= lat_max)
#         lon_mask = (dataT['lon'] >= lon_min) & (dataT['lon'] <= lon_max)

#         # x_min, x_max = 4028021.5446245037, 4323286.106748987 
#         # y_min, y_max = 2641848.5195006253, 3023612.604380675 
#         # x_indices = (dataT.x >= x_min) & (dataT.x <= x_max)
#         # y_indices = (dataT.y >= y_min) & (dataT.y <= y_max)
#         cropped_data = dataT.isel(lat=lat_mask, lon=lon_mask)

#         lat = f.variables["lat"][:]
#         lon = f.variables["lon"][:]
#         time = f.variables['time'][:]
#         days = len(time)


#         Array[days_loop:(days_loop+days), :, :] = np.float32(cropped_data[var][:, :, :])
#         days_loop += days
#         print(days_loop)
#         print(days)


# """Create a new netCDF file"""
# output_directory = "C:/03_Capstone/Data/Future/historical/tasmin_his/"
# output_file = "his_tasmin_1950-2014.nc"

# with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
#     time = ds.createDimension('time', all_days)
#     lon = ds.createDimension('lon', 6)  # Corrected dimension name
#     lat = ds.createDimension('lat', 11)  # Corrected dimension name

#     times = ds.createVariable('time', 'f4', ('time',))
#     lons = ds.createVariable('lon', 'f4', ('lon',))  # Corrected variable name
#     lats = ds.createVariable('lat', 'f4', ('lat',))  # Corrected variable name
#     value = ds.createVariable(var, 'f4', ('time', 'lon', 'lat'))  # Corrected variable names

#     value.units = 'Unknown'

#     # Use the specified boundaries for lons and lats
#     lons[:] = np.linspace( 51, 54, 6)
#     lats[:] = np.linspace(10, 15, 11)
#     times[:] = np.arange(0, all_days, 1)

#     value[:, :, :] = Array

        

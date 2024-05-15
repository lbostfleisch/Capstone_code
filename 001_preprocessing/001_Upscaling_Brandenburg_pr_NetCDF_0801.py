"""the version of this code is from:12.03.2024
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
directory = "C:/03_Capstone/Data/Python_NetCDF_join/DWD CDC/precipitation_nc/Output"

var = "pr"
lat_max = 3023612.5
lat_min = 2641848.5
lon_max = 4323286.0
lon_min =  4028021.5  
lat_length = int((lat_max - lat_min)//5000) + 1
print(f"lat len: {lat_length}")
lon_length = int((lon_max - lon_min)//5000) 
print(f"lon len: {lon_length}")

all_days = (365 * 45) + 11 #for the data from 1970-2014
print(all_days)
days_loop = 0

Array = np.zeros((all_days, lon_length , lat_length), dtype=np.float32)

"File to loop the observed pr files together, upscale, and save them"
for i in range(1970, 2014+1, 1):
    drive = "C:/" 
    directory = "03_Capstone/Data/Python_NetCDF_join/DWD CDC/precipitation_nc/download/" 
    year = i
    var = "pr"
    file_name = f"pr_hyras_1_{i}_v5-0_de.nc"
    file_path = os.path.join(drive, directory, file_name)

    with xr.open_dataset(file_path) as f:
        # Crop the data
        x_min, x_max = lon_min, lon_max
        y_min, y_max = lat_min, lat_max
        # ds_cropped = ds.sel(x=slice(x_min, x_max), y=slice(y_min, y_max))
        x_indices = (f.x >= x_min) & (f.x <= x_max)
        y_indices = (f.y >= y_min) & (f.y <= y_max)
        cropped_data = f.isel(x=x_indices, y=y_indices)
        

        # Resample to 5km x 5km resolution
        resampled_data = cropped_data.interp(method='linear', x=np.linspace(lon_min, lon_max, lon_length),
                                     y=np.linspace(lat_min, lat_max, lat_length))
        resampled_data = resampled_data.transpose('time', 'x', 'y', 'bnds')

        time = f.variables['time'][:]
        lon = f.variables["lon"][:]
        lat = f.variables["lat"][:]
        days = len(time)

        Array[days_loop:(days_loop+days), :, :] = np.float32(resampled_data[var][:, :, :])
        days_loop += days
        print(days_loop)
        print(days)

"""Create a new netCDF file"""
output_directory = "C:/03_Capstone/Data/Python_NetCDF_join/DWD CDC/precipitation_nc/Output"
output_file = "pr_1970-2014_5km.nc"

with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days)
    lon = ds.createDimension('lon', lon_length) # Corrected dimension name
    lat = ds.createDimension('lat', lat_length)  # Corrected dimension name

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('lon', 'f4', ('lon',))  # Corrected variable name
    lats = ds.createVariable('lat', 'f4', ('lat',))  # Corrected variable name
    value = ds.createVariable(var, 'f4', ('time', 'lon', 'lat')) # Corrected variable names

    value.units = 'mm'

    # Use the specified boundaries for lons and lats
    times[:] = np.arange(0, all_days, 1)
    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max, lat_length)
    print(Array.shape)
    value[:, :, :] = Array

print("File was successfuly upscaled and saved!! :)")
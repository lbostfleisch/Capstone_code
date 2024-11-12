"""
Testing the rotation 
07.11.2024
"""

import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
from scipy.interpolate import griddata
from cordex.grid import Grid
from cordex.grid import rotated_grid_transform
import xarray as xr
from netCDF4 import Dataset
import os





# Load your NetCDF data file
file_path = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/original_files/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19660101-19701231.nc'  # Replace with your actual file path
dataset = nc.Dataset(file_path)

# Extract rotated coordinates and data variable
rot_lon_arr = dataset.variables['rlon'][:]
rot_lat_arr = dataset.variables['rlat'][:]
data_variable = dataset.variables['pr'][:]  # Replace 'data_variable' with your actual variable name
print("data variabl",data_variable.shape)


"try 2 "
# ds = xr.open_dataset(file_path)
# lon_rot = ds['rlon'].values
# lat_rot = ds['rlat'].values

nc_file = Dataset(file_path, 'r')
lon_rot = nc_file.variables['lon']
lat_rot = nc_file.variables['lat']

rotated_grid_nc = rotated_grid_transform(lon_arr=lon_rot, lat_arr=lat_rot, np_lon=39.25, np_lat=198, direction="rot2geo")
lon_geo, lat_geo = rotated_grid_nc

# # Initialize rotated Grid and transform to geographic coordinates
# rotated_grid = Grid(lon_arr=rot_lon_arr, lat_arr=rot_lat_arr, pol_lon=198.0, pol_lat=39.25)
# geo_grid = rotated_grid.transform()

# # # Get transformed coordinates
# geo_lon_arr, geo_lat_arr = geo_grid.get_coordinates_geo()

# # Flatten arrays for interpolation (griddata requires 1D arrays of points)
# rot_lon_flat = rot_lon_arr.flatten()
# # print("rot_lon_flat", rot_lon_flat)
# rot_lat_flat = rot_lat_arr.flatten()
# # print(rot_lat_flat)
# data_flat = data_variable.flatten()
# # print(data_flat)
# geo_lon_flat = geo_lon_arr.flatten()
# # print(geo_lon_flat)
# geo_lat_flat = geo_lat_arr.flatten()
# # print(geo_lat_flat)

# # Interpolate data from rotated to geographic grid
# # Using griddata for nearest-neighbor interpolation
# data_variable_transformed_flat = griddata(
#     (rot_lat_flat, rot_lon_flat), 
#     data_flat, 
#     (geo_lat_flat, geo_lon_flat), method='nearest'
# )

# if data_variable_transformed_flat.size == geo_lon_arr.size:
#     data_variable_transformed = data_variable_transformed_flat.reshape(geo_lon_arr.shape)
# else:
#     raise ValueError("Mismatch in the reshaped data; verify target shapes are consistent.")



output_file_path = 'C:/03_Capstone/a_publishing/data/test_files_rot/1107_type4_test_rot.nc'
all_days = 1826
lon_len = 424
lat_len =  412
Array = np.zeros((all_days, lat_len, lon_len), dtype=np.float32)  
lon_min, lon_max = np.min(lon_geo), np.max(lon_geo)
lat_min, lat_max = np.max(lat_geo), np.max(lat_geo)
Array[:, :, :] = data_variable[:all_days, :lat_len, :lon_len]
# Array[:, :, :] = data_variable[:, :, :]


with Dataset(output_file_path, 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days)
    lon = ds.createDimension('lon', lon_len)  # Corrected dimension name
    lat = ds.createDimension('lat', lat_len)  # Corrected dimension name

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('lon', 'f4', ('lon',))  # Corrected variable name
    lats = ds.createVariable('lat', 'f4', ('lat',))  # Corrected variable name
    value = ds.createVariable('pr', 'f4', ('time', 'lat', 'lon'))  # Corrected variable names

    value.units = 'Unknown'

    # Use the specified boundaries for lons and lats
    lons[:] = np.linspace(lon_min, lon_max, lon_len)
    lats[:] = np.linspace(lat_min, lat_max, lat_len)
    times[:] = np.arange(0, all_days, 1)

    value[:, :, :] = Array
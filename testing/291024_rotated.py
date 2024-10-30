""""
29.10.24
testing rotation from GitHub link: https://github.com/gitter-badger/cordex
"""
import cordex
import logging
import numpy as np
import math

from cordex import __version__

from cordex.grid import rotated_grid_transform
from cordex.grid import Grid

from netCDF4 import Dataset
import xarray as xr

file_path = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/original_files/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19660101-19701231.nc'  # Replace with your actual file path
# file_path = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/tasmin/tasmin_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_1966-2005_degC.nc'
# nc_file = Dataset(file_path, 'r')
# var = nc_file.variables['pr']
# rot_lon = nc_file.variables['rlon']
# rot_lat = nc_file.variables['lat']
# print(rot_lat)

# # transform_test = rotated_grid_transform(np_lon = rot_lon, np_lat=rot_lat)
# # grid_test = Grid(nc_file, lon_arr=nc_file.variables['rlon'], lat_arr=nc_file.variables['rlat'])

ds = xr.open_dataset(file_path)
print(ds)

# Extract rotated grid coordinates
lon_rot = ds['rlon'].values
lat_rot = ds['rlat'].values

# Define the rotated North Pole's coordinates (these values should be specified in your data)
# pol_lon, pol_lat = 198.0, 39.25  # Example values; replace with your actual rotated pole coordinates
pol_lon, pol_lat = 39.25, 198.0  # Example values; replace with your actual rotated pole coordinates

# Create a Grid instance with the rotated coordinates
rot_grid = Grid(lon_rot, lat_rot, pol_lon, pol_lat)

# Transform the rotated grid to geographic coordinates
geo_grid = rot_grid.transform()  # This returns a new Grid instance with regular coordinates

# Get transformed geographic coordinates
lon_geo, lat_geo = geo_grid.get_coordinates()

print("Shape of transformed longitude:", lon_geo.shape)
print("Shape of transformed latitude:", lat_geo.shape)
print("Sample values (geo lon, geo lat):", lon_geo[:5, :5], lat_geo[:5, :5])

# Save the transformed coordinates back to the dataset, or save as a new NetCDF
ds['longitude'] = (('y', 'x'), lon_geo)
ds['latitude'] = (('y', 'x'), lat_geo)

# Optionally, save the modified dataset with new geographic coordinates
ds.to_netcdf("C:/03_Capstone/Capstone_code/testing/test_rot.nc")
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
from cordex.grid import RotGrid

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
# print(ds)

"try 1"
lon_rot = ds['rlon'].values
lat_rot = ds['rlat'].values

# Define the rotated North Pole's coordinates (these values should be specified in your data)
# pol_lon, pol_lat = 198.0, 39.25  # Example values; replace with your actual rotated pole coordinates
pol_lon, pol_lat = 39.25, 198.0  # Example values; replace with your actual rotated pole coordinates
pol_lat != 90
# Create a Grid instance with the rotated coordinates
rot_grid = Grid(lon_rot, lat_rot, pol_lon=pol_lon, pol_lat=pol_lat)
print("rot grid", rot_grid)

geo_grid = rot_grid.transform()  # This returns a new Grid instance with regular coordinates
print("geo grid", geo_grid)
# Get transformed geographic coordinates
lon_geo, lat_geo = geo_grid.get_coordinates()
# print(lon_geo)
# test



"RotGrid Deprecated"
# rot_grid_2 = RotGrid(rot_grid)
# geo_grid_2 = rot_grid_2.rotated_grid_transform(lon_arr=lon_rot, lat_arr=lat_rot, np_lon = pol_lon, np_lat = pol_lat, direction='rot2geo')
# lon_geo_2, lat_geo_2 = geo_grid_2.get_coordinates()

"try 2"
# Nx, Ny = 106, 103 #from the CORDEX website 
# rot_lon_values = np.linspace(331.79, 331.79 + (Nx - 1) * 0.1, Nx)  # Example longitude array for rotated grid
# rot_lat_values = np.linspace(21.67, 21.67 + (Ny - 1) * 0.1, Ny)     # Example latitude array for rotated grid
# rot_lon_arr, rot_lat_arr = np.meshgrid(rot_lon_values, rot_lat_values)

# # Instantiate the Grid class with the rotated pole information
# rotated_grid = Grid(lon_arr=rot_lon_arr, lat_arr=rot_lat_arr, pol_lon=198.0, pol_lat=39.25)

# # Transform to geographical coordinates (non-rotated)
# geo_grid = rotated_grid.transform()

# # Retrieve the transformed coordinates in the standard geographic system
# geo_lon_arr, geo_lat_arr = geo_grid.get_coordinates_geo()

print("Shape of transformed longitude:", lon_geo.shape)
print("Shape of transformed latitude:", lat_geo.shape)
print("Sample values (geo lon, geo lat):", lon_geo[:5, :5], lat_geo[:5, :5])

# Save the transformed coordinates back to the dataset, or save as a new NetCDF
ds['longitude'] = (('y', 'x'), lon_geo)
ds['latitude'] = (('y', 'x'), lat_geo)

# Optionally, save the modified dataset with new geographic coordinates
ds.to_netcdf("C:/03_Capstone/a_publishing/data/test_files_rot/1107_test_rot.nc")
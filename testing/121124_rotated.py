"""
rotation file 12.11.24
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

#parameteres from the cordex website: https://cordex.org/domains/cordex-region-euro-cordex/
rot_pole_lat = 198
rot_pole_lon = 39.25
TLC_lat = 331.79
TLC_lon = 21.67
Nx = 106
Ny = 103

file_path = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/original_files/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19660101-19701231.nc'  # Replace with your actual file path
dataset = nc.Dataset(file_path)

rot_lon_arr = dataset.variables['rlon'][:]
rot_lat_arr = dataset.variables['rlat'][:]
data_variable = dataset.variables['pr'][:]  
print("data variabl",data_variable.shape)

nc_file = Dataset(file_path, 'r')
lon_rot = nc_file.variables['lon']
lat_rot = nc_file.variables['lat']

rotated_grid_nc = rotated_grid_transform(lon_arr=lon_rot, lat_arr=lat_rot, np_lon=rot_pole_lon, np_lat=rot_pole_lat, direction="rot2geo")
lon_geo, lat_geo = rotated_grid_nc
# lon_geo = lon_geo[:Nx, :Ny]
# lat_geo = lat_geo[:Nx, :Ny]

if lon_geo.shape != (Ny, Nx) or lat_geo.shape != (Ny, Nx):
    lon_geo = lon_geo[:Ny, :Nx]
    lat_geo = lat_geo[:Ny, :Nx]
    
print("Geographic longitude extents:", np.min(lon_geo), np.max(lon_geo))
print("Geographic latitude extents:", np.min(lat_geo), np.max(lat_geo))

output_file_path = 'C:/03_Capstone/a_publishing/data/test_files_rot/1211_type3_test_rot.nc'
all_days = 1826
# lon_len = 424
# lat_len =  412
# Array = np.zeros((all_days, lat_len, lon_len), dtype=np.float32)  
lon_min, lon_max = np.min(lon_geo), np.max(lon_geo)
lat_min, lat_max = np.max(lat_geo), np.max(lat_geo)
# Array[:, :, :] = data_variable[:all_days, :lat_len, :lon_len]
Array = np.zeros((all_days, Nx, Ny), dtype=np.float32)
# Array[:, :, :] = data_variable[:all_days, :Nx, :Ny]
try:
    Array[:, :, :] = data_variable[:all_days, :Nx, :Ny]
    print("Array filled successfully.")
except ValueError as e:
    print("Error in filling Array:", e)


with Dataset(output_file_path, 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days)
    lon = ds.createDimension('lon', Ny)  
    lat = ds.createDimension('lat', Nx)  

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('lon', 'f4', ('lon',)) 
    lats = ds.createVariable('lat', 'f4', ('lat',))  
    value = ds.createVariable('pr', 'f4', ('time', 'lat', 'lon')) 

    value.units = 'Unknown'
    # lons[:] = np.linspace(lon_min, lon_max, Ny)
    # lats[:] = np.linspace(lat_min, lat_max, Nx)
    lons[:] = lon_geo[0, :]
    lats[:] = lat_geo[:, 0]
    times[:] = np.arange(0, all_days, 1)

    value[:, :, :] = Array
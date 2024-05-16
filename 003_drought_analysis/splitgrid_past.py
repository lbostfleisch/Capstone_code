"""
purpose: regridding the past modelled data to the resolution of the past modelled data 
author: Luca Boestfleisch 
last updated: 23.04.24
"""

from netCDF4 import Dataset
import numpy as np

low_res_nc = Dataset('', 'r') #adapt 
output_path = '' #adapt

low_res_lat = len(low_res_nc.dimensions['lat'])
low_res_lon = len(low_res_nc.dimensions['lon'])
low_res_time = len(low_res_nc.dimensions['time'])

'define the ratio between the two files (lat and lon)'
lat_ratio = 11  #adapt
lon_ratio = 6  #adapt

high_res_lat = low_res_lat * lat_ratio
print(high_res_lat)
high_res_lon = 59

low_res_data = low_res_nc.variables['spei'][:] #adapt the variable name 

'reshape the lowresolution data to more gridcells'
reshaped_low_res_data = np.repeat(np.repeat(low_res_data, lon_ratio, axis=1), lat_ratio, axis=2)

split_nc = Dataset(output_path, 'w', format='NETCDF4')

split_nc.createDimension('time', low_res_time)
split_nc.createDimension('lon', high_res_lon)
split_nc.createDimension('lat', high_res_lat)

time_var = split_nc.createVariable('time', 'f4', ('time',))
time_var[:] = low_res_nc.variables['time'][:]

lat_var = split_nc.createVariable('lat', 'f4', ('lat',))
lat_var[:] = np.linspace(low_res_nc.variables['lat'][0], low_res_nc.variables['lat'][-1], high_res_lat)

lon_var = split_nc.createVariable('lon', 'f4', ('lon',))
lon_var[:] = np.linspace(low_res_nc.variables['lon'][0], low_res_nc.variables['lon'][-1], high_res_lon)

spei_split_var = split_nc.createVariable('spei_split', 'f4', ('time', 'lon', 'lat'))

spei_split_var[:] = reshaped_low_res_data

# Close the NetCDF files
low_res_nc.close()
split_nc.close()

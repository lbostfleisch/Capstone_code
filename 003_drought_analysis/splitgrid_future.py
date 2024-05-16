"""
purpose: regridding the future modelled data to the resolution of the past modelled data 
author: Luca Boestfleisch 
last updated: 20.04.24
"""

from netCDF4 import Dataset
import numpy as np

# Open the NetCDF file
low_res_nc = Dataset('', 'r') #adapt 
output_path = '' #adapt 

low_res_lat = len(low_res_nc.dimensions['lat'])
low_res_lon = len(low_res_nc.dimensions['lon'])
# low_res_time = len(low_res_nc.dimensions['time'])

"define the ratio of the two files below "
lat_ratio = 11  # Change this to your desired ratio
lon_ratio = 6  # Change this to your desired ratio

high_res_lat = low_res_lat * lat_ratio
high_res_lon = low_res_lon * lon_ratio
low_res_data = low_res_nc.variables['spei_avg'][:] #adapt 

'reshape the dimensions to match the past data'
reshaped_low_res_data = np.repeat(np.repeat(low_res_data, lon_ratio, axis=0), lat_ratio, axis=1)

"create a new netcdf file"
split_nc = Dataset(output_path, 'w', format='NETCDF4')

# split_nc.createDimension('time', low_res_time) #uncomment this code if there is a time variable present 
split_nc.createDimension('lon', high_res_lon)
split_nc.createDimension('lat', high_res_lat)

'uncomment below if there is a time variable'
# time_var = split_nc.createVariable('time', 'f4', ('time',))
# time_var[:] = low_res_nc.variables['time'][:]

lat_var = split_nc.createVariable('lat', 'f4', ('lat',))
lat_var[:] = np.linspace(low_res_nc.variables['lat'][0], low_res_nc.variables['lat'][-1], high_res_lat)

lon_var = split_nc.createVariable('lon', 'f4', ('lon',))
lon_var[:] = np.linspace(low_res_nc.variables['lon'][0], low_res_nc.variables['lon'][-1], high_res_lon)

# spei_split_var = split_nc.createVariable('spei_split', 'f4', ('time', 'lon', 'lat')) #uncomment if there is a time variable
spei_split_var = split_nc.createVariable('spei_split', 'f4', ('lon', 'lat'))

spei_split_var[:] = reshaped_low_res_data

low_res_nc.close()
split_nc.close()

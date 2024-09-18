"""
purpose: cropping the future files to extent of brandenburg, reprojecting the files to the LCC Europe climate projections and looping the files together 
last accessed: 12.03.24
author: Luca Boestfleisch (with parts adopted from Joeri Reinders)

note: some file paths need to be adapted for the code to run (see '#adapt' comment)
"""


import xarray as xr
from pyproj import Proj, Transformer
import os
import numpy as np
from netCDF4 import Dataset
import netCDF4

"First: cropping the file down to the desired lat/lon in WGS84"
# drive = "C:/" #adapt
# directory = "03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/"  #adapt
# file = "pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_7.nc" #adapt
# file_path = os.path.join(drive, directory, file)

# with Dataset(file_path, 'r') as nc:
#     # Display dimensions
#     for dimname, dim in nc.dimensions.items():
#         print(f"Dimension: {dimname}, Size: {len(dim)}")

#     # Display variables
#     for varname, var in nc.variables.items():
#         print(f"Variable: {varname}, Shape: {var.shape}")

#     for varname, var in nc.variables.items():
#         print(f"Variable: {varname}, Shape: {var.shape}")

#         # Check if the variable is longitude or latitude
#         if 'lon' in varname.lower():
#             print(f"Min Longitude: {var[:].min()}, Max Longitude: {var[:].max()}")
#         elif 'lat' in varname.lower():
#             print(f"Min Latitude: {var[:].min()}, Max Latitude: {var[:].max()}")


# """code to crop the file down to given lat/lon extents"""

# days_loop = 0 
# loaded_data = xr.open_dataset(file_path)

# "below: CMIP6 Capstone coordinates"
# lat_min, lat_max = 49, 56 #adapt
# lon_min, lon_max = 9, 15.5 #adapt

# # "below: CMIP5 coordinates: for rotated coordinate system"
lat_min, lat_max = -6.0, 8.0
lon_min, lon_max = -8.0, -1.0

# lon_mask = (loaded_data['rlon'] >= lon_min) & (loaded_data['rlon'] <= lon_max)
# lat_mask = (loaded_data['rlat'] >= lat_min) & (loaded_data['rlat'] <= lat_max)

# cropped_data = loaded_data.sel( rlon = lon_mask, rlat = lat_mask )
# # cropped_data = cropped_data.transpose('time', 'rlon', 'rlat', 'axis_nbounds') #old: 'axis_nbounds' only applicable to CMIP6
# # cropped_data = cropped_data.transpose('time', 'rlon', 'rlat', 'bnds') 
# cropped_data = cropped_data.transpose('time', 'bnds', 'rlon', 'rlat', 'vertices') 


# # save the data 
# output_drive = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr" #adapt
# output_file = "pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_7_cropped.nc"#adapt
# output_path = os.path.join(output_drive, output_file)

# cropped_data.to_netcdf(output_path, format='NETCDF4')
# print("cropped and saved the initial file!")


# #########################################################################

"reprojecting the file"
"Load the NetCDF file in WGS84"
# input_file = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/pr/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day_19660101-19701231.nc'#adapt
# # input_file = "C:/03_Capstone/Data/Future/historical/pr_his/his_pr_1950-2014_EPSG3034.nc"
# output_file = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/pr/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day_19660101-19701231_epsg3034.nc'#adapt


# # Step 3: Reproject Coordinates (if needed)
# # source_proj = Proj(proj='latlong', datum='WGS84')
# target_proj = Proj(init='epsg:3034')

# transformer = Transformer.from_proj(source_proj, target_proj)
# lon, lat = transformer.transform(ds.lon.values.flatten(), ds.lat.values.flatten())

# # Reshape lon and lat to 2D arrays
# lon_2d = lon.reshape(ds.lon.shape)
# lat_2d = lat.reshape(ds.lat.shape)

# ds['lon'] = xr.DataArray(lon_2d, dims=['lon'])
# ds['lat'] = xr.DataArray(lat_2d, dims=['lat'])

# # Use the interp method with coord parameter
# ds_resampled = ds.interp(coords={'lon': ds['lon'], 'lat': ds['lat']}, method='linear')

# # Save the final dataset to a new NetCDF file
# ds_resampled.to_netcdf(output_file)
# print("File reprojected to LCC Europe EPSG3034 and saved! :) ")

# # ##################################################
"Then: crop down to the exact same coordinates as the obs data"
"CMIP6"
# lon_max = 4323286.0
# lon_min =  4028021.5  
# lat_max = 3023612.5
# lat_min = 2641848.5
# lon_length = 10
# lat_length = 7

# "CMIP5"
lon_length = 63
lat_length = 128

# output_directory_EPSG3034 = ""#adapt
# output_file_EPSG3034 = ""#adapt
# output_path_EPSG3034 = os.path.join(output_directory_EPSG3034, output_file_EPSG3034)

# file_path = ""#adapt
# loaded_data = xr.open_dataset(file_path)

# lon_mask = (loaded_data['lon'] >= lon_min) & (loaded_data['lon'] <= lon_max)
# lat_mask = (loaded_data['lat'] >= lat_min) & (loaded_data['lat'] <= lat_max)

# cropped_data = loaded_data.sel( lon = lon_mask, lat = lat_mask )
# cropped_data = cropped_data.transpose('time', 'lon', 'lat', 'axis_nbounds')

# cropped_data.to_netcdf(output_path_EPSG3034, format='NETCDF4')
# print("cropped down to the exact observational boundaries (EPSG 3034) and saved!")

##########################################
"Then: loop the files together"
"CMIP6"
# all_days_join = 9131 + 9132 + 9131 + 4017

"CMIP5"
all_days_join = 1826 + 1826 + 1827 + 1826 + 1826 + 1826 + 1827 + 1826 
print("all_days_join",all_days_join )
days_loop = 0
Array = np.zeros((all_days_join, lon_length , lat_length), dtype=np.float32) 

for i in range(8):
    var = "pr"#adapt
    file_name = f"pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_{i}_cropped.nc"#adapt
    file_path = os.path.join("C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr", file_name)

    with Dataset(file_path, 'r') as f:
        dataT = xr.open_dataset(file_path)
        lat_mask = (dataT['rlat'] >= lat_min) & (dataT['rlat'] <= lat_max)
        lon_mask = (dataT['rlon'] >= lon_min) & (dataT['rlon'] <= lon_max)
        cropped_data = dataT.isel(rlon=lon_mask, rlat=lat_mask)

        time = f.variables['time'][:]
        lon = f.variables["rlon"][:]
        lat = f.variables["rlat"][:]
        days = len(time)


        Array[days_loop:(days_loop+days), :, :] = np.float32(cropped_data[var][:, :, :])

        days_loop += days
        print(days_loop)
        print(days)


"""Create a new netCDF file"""
output_directory_joined = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr"#adapt
output_file = "pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_1966-2005_joined.nc"#adapt

with Dataset(os.path.join(output_directory_joined, output_file), 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days_join)
    lon = ds.createDimension('lon', lon_length)  # Corrected dimension name
    lat = ds.createDimension('lat', lat_length)  # Corrected dimension name

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('lon', 'f4', ('lon',))  # Corrected variable name
    lats = ds.createVariable('lat', 'f4', ('lat',))  # Corrected variable name
    value = ds.createVariable(var, 'f4', ('time', 'lon', 'lat'))  # Corrected variable names

    value.units = 'Unknown'

    # Use the specified boundaries for lons and lats
    times[:] = np.arange(0, all_days_join, 1)
    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max, lat_length)
    print(Array.shape)
    value[:, :, :] = Array


print("saved the joined file!! :)")

# ##########################################################3
"Last step: Crop the joined data down to 1970-2014 (including both years)"

# input_path_time = ""#adapt
# var = "pr" #adapt
# # input_data = Dataset(input_path, 'r')
# input_data_time = xr.open_dataset(input_path_time)
# for varname in input_data_time.variables:
#     print(f"Variable: {varname}")
# print(input_data_time)

# lon = input_data_time.variables['lon'][:]
# lat = input_data_time.variables['lat'][:]
# time = input_data_time.variables['time'][:]
# min_lon, max_lon, min_lat, max_lat = lon.min(), lon.max(), lat.min(), lat.max()

# """
# Modelled historical: Temperature (tasmin, tasmax) & Precipitation 
#     note on the days calculation for modelled historical data: range from 1950-2014 (incl.) and want to crop it to 1970-2014
#     1970-1950 = 20 years , in that time period # of leap years = 5
#     18262 + 5479 

# Observed Precipitation (pr)
#     file goes from 1991-2020 => so need to remove the last years 
#     want to have 24 years (including 6 leap days)


# """
# start_day = (20 * 365 ) + 5 ###########modelled historical  
# end_day = len(time)   ###########modelled historical 
# # start_day = 0 ############# obserbed DWD precipitation 
# # end_day = (24 * 365) + 6 ############# obserbed DWD precipitation 

# print(f"end day: {end_day}")

# tot_days = end_day - start_day
# # check_day = (18262 + 5479) - tot_days
# control_period = (45 * 365) + 11
# print(f"total days: {tot_days}")
# # print(f"check: {check_day}")
# print(f"control period: {control_period}")

# cropped_dataset = input_data_time.sel(time=slice(start_day, end_day))
# cropped_dataset = cropped_dataset.reset_index('time', drop=False)
# # Save the cropped dataset to a new NetCDF file if needed
# cropped_dataset.to_netcdf('')#adapt

# # Close the original dataset
# input_data_time.close()
# print("Data cropped down to the wanted timestep successfully!")
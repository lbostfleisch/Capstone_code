"testing cropping"
import rasterio
import xarray as xr
from rasterio.enums import Resampling
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import os

drive = "C:/" ###### ADAPT THIS! 
# directory = "03_Capstone/Data/Future/historical/tasmax_his/"  ###### ADAPT THIS! 
directory = "03_Capstone/Data/Future/historical/tasmax_his/"
# input_obs = "C:/03_Capstone/Data/Python_NetCDF_join/DWD CDC/precipitation_nc/Output/reproject_test_0903_transformed.nc"
# input_his = "C:/03_Capstone/Data/Future/historical/pr_his/his_pr_1975-2014.nc"
# file = "tasmax_day_CNRM-CM6-1-HR_historical_r1i1p1f2_gr_20000101-20141231.nc" ###### ADAPT THIS! 
file = "tasmax_day_CNRM-CM6-1-HR_historical_r1i1p1f2_gr_19500101-19991231.nc"

# #C:\03_Capstone\Data\Future\cropped_data\pr
file_path = os.path.join(drive, directory, file)

with Dataset(file_path, 'r') as nc:
    # Display dimensions
    for dimname, dim in nc.dimensions.items():
        print(f"Dimension: {dimname}, Size: {len(dim)}")

    # Display variables
    for varname, var in nc.variables.items():
        print(f"Variable: {varname}, Shape: {var.shape}")

    for varname, var in nc.variables.items():
        print(f"Variable: {varname}, Shape: {var.shape}")

        # Check if the variable is longitude or latitude
        if 'lon' in varname.lower():
            print(f"Min Longitude: {var[:].min()}, Max Longitude: {var[:].max()}")
        elif 'lat' in varname.lower():
            print(f"Min Latitude: {var[:].min()}, Max Latitude: {var[:].max()}")


"""code to crop the file down to given lat/lon extents"""

days_loop = 0 
loaded_data = xr.open_dataset(file_path)

lat_min, lat_max = 49, 56
lon_min, lon_max = 9, 15.5

# Create boolean masks for latitude and longitude
lon_mask = (loaded_data['lon'] >= lon_min) & (loaded_data['lon'] <= lon_max)
lat_mask = (loaded_data['lat'] >= lat_min) & (loaded_data['lat'] <= lat_max)



# Crop the data based on boolean masks
cropped_data = loaded_data.sel( lon = lon_mask, lat = lat_mask )
cropped_data = cropped_data.transpose('time', 'lon', 'lat', 'axis_nbounds')


# Save the cropped data to a new NetCDF file
output_drive = "C:/03_Capstone/Data/Future/historical/tasmax_his/"
output_file = "cropped_tasmax_day_CNRM-CM6-1-HR_historical_r1i1p1f2_gr_19500101-19991231.nc"
output_path = os.path.join(output_drive, output_file)

cropped_data.to_netcdf(output_path, format='NETCDF4')
print("cropped and saved!")

# # #######################################################################################################################
"Code to crop it down to the period 1991-2014 (inclusive)"
input_path = "C:/03_Capstone/Data/Future/historical/pr_his/his_pr_mm_1975-2014.nc"
var = "pr" ## ADAPT HERE 
# input_data = Dataset(input_path, 'r')
input_data = xr.open_dataset(input_path)
for varname in input_data.variables:
    print(f"Variable: {varname}")

print(input_data)

lon = input_data.variables['lon'][:]
lat = input_data.variables['lat'][:]
time = input_data.variables['time'][:]
min_lon, max_lon, min_lat, max_lat = lon.min(), lon.max(), lat.min(), lat.max()


"""
Modelled historical: Temperature (tasmin, tasmax)
    note on the days calculation for modelled historical data: range from 1950-2014 (incl.) and want to crop it to 1991-2014
    1991-1950 = 41 years, in that time period # of leap years = 10
    18262 + 5479 

Observed Precipitation (pr)
    file goes from 1991-2020 => so need to remove the last years 
    want to have 24 years (including 6 leap days)

Modelled historical: Precipitation (pr) 
    file goes from 1975-2014 => so need to remove the initial years 
    want to have 16 years removed from the beginning. Adding 5 days becayse of leap days 
"""
# start_day = (41 * 365 ) + 10 ###########modelled historical temp 
# end_day = len(time)   ###########modelled historical temp
# start_day = 0 ############# obserbed DWD precipitation 
# end_day = (24 * 365) + 6 ############# obserbed DWD precipitation 
start_day = (16 * 365) + 4   ############# modelled his precipitation 
end_day = len(time)   ############# modelled his precipitation 

print(f"end day: {end_day}")

tot_days = end_day - start_day
# check_day = (18262 + 5479) - tot_days
control_period = (24 * 365) + 6 
print(f"total days: {tot_days}")
# print(f"check: {check_day}")
print(f"control period: {control_period}")

cropped_dataset = input_data.sel(time=slice(start_day, end_day))
cropped_dataset = cropped_dataset.reset_index('time', drop=False)
# Save the cropped dataset to a new NetCDF file if needed
cropped_dataset.to_netcdf('C:/03_Capstone/Data/Future/historical/pr_his/his_pr_mm_1991-2014.nc')

# Close the original dataset
input_data.close()
print("Data cropped down to the wanted timestep successfully!")
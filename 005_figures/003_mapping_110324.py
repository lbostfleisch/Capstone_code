"""
test: visualization/mapping 
11.3.2024
"""

import os
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# File information
# C:\03_Capstone\a_publishing\data\CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17\r12i1p1_v1\pr\rotated_files
drive = "C:/"
directory = "03_Capstone/a_publishing/data/test_files_rot/"
# directory = "03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/original_files/"
# directory = '03_Capstone/Data/Future/ssp126/tasmax/'
file = "1911_type2_test_rot.nc"
# file = 'pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19660101-19701231.nc'
# file = "cropped2_tasmax_day_CNRM-CM6-1-HR_ssp126_r1i1p1f2_gr_0.nc"
# C:/03_Capstone/Data/Downscale/downscale_test_040424.nc

"other drive"
# drive = 'D:/'
# directory = 'Luca_Capstone/data/cmip6_ssp126/tasmax/big_files/'
# file = 'tasmax_day_CNRM-CM6-1-HR_ssp126_r1i1p1f2_gr_20150101-20641231.nc'

variable_name = 'pr'
file_path = os.path.join(drive, directory, file)

# file_path = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/original_files/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19660101-19701231.nc'

# Open the NetCDF dataset
data = xr.open_dataset(file_path)



########################################################################
"To plot when the data has time, lon, lat"
time_index = 0

# 16435 past 
# 31411 future 

# Extract the variable for the chosen time step

variable = data[variable_name].isel(time=time_index)
"for pentad data"
# variable = data[variable_name].isel(pentad=time_index)

print(variable.shape)

print(f"Min Latitude: {variable.lat.min().values}, Max Latitude: {variable.lat.max().values}")
print(f"Min Longitude: {variable.lon.min().values}, Max Longitude: {variable.lon.max().values}")

# Plot the variable
fig, ax = plt.subplots()
# variable.plot.imshow(x="lon", y='lat', ax=ax)
# variable.plot.imshow(x="lat", y='lon', ax=ax)

variable.plot(ax=ax)


# Customize the plot if needed
plt.title(f'{variable_name} at time {time_index}')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Show the plot
plt.show()
print(variable)


###########################
"when the data only has lon/lat"
# variable = data[variable_name]
# print("Dimensions:", variable_name)
# # print(data[variable_name].isel(time=time_index))

# #min and max values for the color scale
# min_color =30
# max_color = 40
# level_color = 256
# if np.any(~np.isfinite(variable)):
#     print("Warning: Data contains non-finite values (NaN or infinity). Preprocessing data...")
#     # Replace non-finite values with NaN
#     variable = variable.where(np.isfinite(variable), np.nan)

# # Continue with plotting code
# print("Dimensions:", variable_name)

# if 'lat' in variable.dims and 'lon' in variable.dims:
#     # Print latitude and longitude range
#     print(f"Min Latitude: {variable.lat.min().values}, Max Latitude: {variable.lat.max().values}")
#     print(f"Min Longitude: {variable.lon.min().values}, Max Longitude: {variable.lon.max().values}")

#     # Plot the variable
#     fig, ax = plt.subplots()
#     img = variable.plot.imshow(x="lon", y='lat', ax=ax, vmin = min_color, vmax=max_color, cmap='bwr')
#     cbar = plt.colorbar(img, orientation='horizontal')
#     cbar.set_label('SPEI values')

#     plt.title(f'{variable_name}')
#     plt.xlabel('Longitude')
#     plt.ylabel('Latitude')

#     # Show the plot
#     plt.show()
# else:
#     print("The NetCDF file does not have 'lat' and 'lon' dimensions.")

# ######################
"""
figure for downscaling: 15th july 
06.05.24
"""

import os
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import pyproj
from matplotlib.colors import LinearSegmentedColormap
import re

file_info = [
    {"directory": "C:/03_Capstone/Data/Downscale/ssp126", "file": "downscale_ssp126_050524_lr001_bs128_hs300_dp5_epoch200.nc", "variable_name": "predicted_spei", "time": "195"}, #2015
    {"directory": "C:/03_Capstone/Data/Downscale/ssp126", "file": "downscale_ssp126_050524_lr001_bs128_hs300_dp5_epoch200.nc", "variable_name": "predicted_spei", "time": "7500"},  #2035
    {"directory": "C:/03_Capstone/Data/Downscale/ssp126", "file": "downscale_ssp126_050524_lr001_bs128_hs300_dp5_epoch200.nc", "variable_name": "predicted_spei", "time": "14805"}, #2055
    {"directory": "C:/03_Capstone/Data/Downscale/ssp126", "file": "downscale_ssp126_050524_lr001_bs128_hs300_dp5_epoch200.nc", "variable_name": "predicted_spei", "time": "22110"}, #2075
    {"directory": "C:/03_Capstone/Data/Downscale/ssp126", "file": "downscale_ssp126_050524_lr001_bs128_hs300_dp5_epoch200.nc", "variable_name": "predicted_spei", "time": "31242"}, #2100



    {"directory": "C:/03_Capstone/Data/Downscale/ssp585", "file": "downscale_ssp585_050524_lr001_bs128_hs300_dp5_epoch200.nc", "variable_name": "predicted_spei", "time": "195"}, #2015
    {"directory": "C:/03_Capstone/Data/Downscale/ssp585", "file": "downscale_ssp585_050524_lr001_bs128_hs300_dp5_epoch200.nc", "variable_name": "predicted_spei", "time": "7500"}, #2035
    {"directory": "C:/03_Capstone/Data/Downscale/ssp585", "file": "downscale_ssp585_050524_lr001_bs128_hs300_dp5_epoch200.nc", "variable_name": "predicted_spei", "time": "14805"}, #2055
    {"directory": "C:/03_Capstone/Data/Downscale/ssp585", "file": "downscale_ssp585_050524_lr001_bs128_hs300_dp5_epoch200.nc", "variable_name": "predicted_spei", "time": "22110"}, #2075
    {"directory": "C:/03_Capstone/Data/Downscale/ssp585", "file": "downscale_ssp585_050524_lr001_bs128_hs300_dp5_epoch200.nc", "variable_name": "predicted_spei", "time": "31242"}, #2100



]

"""
list of time indices for july 15th 
    2015: 196
    2035: 7496
    2055: 14796
    2075: 22096
    2100: 31221

"""

#TO DO: still need to account for the leap years!! 

# print(196+(365*85))
# print(31411-31221)
# print(365-190)

b = 0

for year in range (2015, 2100+1, 1):
    a = 2015 - year
    if a == 0: 
        day = 195 #although it is the 196th day (July 15), python starts counting at 0, so it is the 195th day in python 
    elif ((a + 1)%4) == 0:  #+1 because 2016 is a leap year 
        day += 366
    else: 
        day += 365
    if year == 2015 or year == 2035 or year ==2055 or year==2075 or year ==2100:
        print(f"year: {year}, day of July 25: {day}")    
    t = day 
    b += 1

num_rows = 2
num_cols = 5

#check to see if the calculation was correct:
print(31411-31242)
print(365-169) #=> should be 196 to represent the 196th day in the year => it does! 


fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 20))
# plt.subplots_adjust(wspace=0, hspace=0) 
# plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)  # Adjust margins around subplots

# Flatten the axes array for easier iteration
axes = axes.flatten()

sm = plt.cm.ScalarMappable(cmap="bwr_r")
sm.set_array([])

minvalue = 2
maxvalue =-2

for i in range(num_rows):
    row_axes = axes[i*num_cols: (i+1)*num_cols]  # Axes for the current row

    # Initialize variables to store the minimum and maximum values for the current row
    min_val = np.inf
    max_val = -np.inf

    for j, source_info in enumerate(file_info[i*num_cols: (i+1)*num_cols]):
        # Adjust the index in file_info to match the current row
        directory = source_info["directory"]
        file = source_info["file"]
        variable_name = source_info["variable_name"]
        time_index = source_info['time']
        file_path = os.path.join(directory, file)

        data = xr.open_dataset(file_path)
        shapefile_path = 'C:/03_Capstone/Data/Analysis/shapefile_br/br_shapefile.shp'
        gdf = gpd.read_file(shapefile_path)

        # Reproject the shapefile
        gdf_reprojected = gdf.to_crs(epsg=3034)
        output_shapefile_path = "C:/03_Capstone/Data/Analysis/shapefile_br/br_shapefile_epsg3034.shp"
        gdf_reprojected.to_file(output_shapefile_path)
        gdf = gpd.read_file(output_shapefile_path)
        
        variable = data[variable_name].isel(time=int(time_index))
        # Extract the variable
        

        # Plot the variable
        # Plot the variable
        # ax = axes[i]
        # variable.plot.imshow(x="lon", y='lat', ax=ax, vmin=minvalue, vmax=maxvalue, cmap="bwr_r")
        # gdf.plot(ax=ax, facecolor='none', edgecolor='black')
        # # ax.set_title(title, fontsize=8)
        # ax.set_xlabel('Longitude', fontsize=8)
        # ax.set_ylabel('Latitude', fontsize=8)
        # ax.annotate('', xy=(0.95, 0.95), xycoords='axes fraction', xytext=(0.95, 0.85),
        #             arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=2))
        # ax.text(0.95, 0.95, 'N', transform=ax.transAxes, ha='center', va='center', fontsize=8,)

        # Plot the variable
        ax = row_axes[j]
        variable.plot.imshow(x="lon", y='lat', ax=ax, cmap="bwr_r")
        gdf.plot(ax=ax, facecolor='none', edgecolor='black')
        ax.set_xlabel('Longitude', fontsize=6)
        ax.set_ylabel('Latitude', fontsize=6)
        ax.set_title("")
        ax.annotate('', xy=(0.95, 0.95), xycoords='axes fraction', xytext=(0.95, 0.85),
                    arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=2))
        ax.text(0.95, 0.95, 'N', transform=ax.transAxes, ha='center', va='center', fontsize=8,)
        ax.tick_params(axis='both', which='major', labelsize=5)  # Adjust the font size of the tick marks

        ax.xaxis.get_major_formatter().set_powerlimits((0, 1))  # Set the power limits for x-axis
        ax.yaxis.get_major_formatter().set_powerlimits((0, 1))  # Set the power limits for y-axis
        ax.xaxis.set_tick_params(labelsize=6)
        ax.yaxis.set_tick_params(labelsize=6)
        title = variable_name.replace("time = ", "")

    # cbar_ax = fig.add_axes([0.95, 0.8, 0.02, 0.15])  # Adjust position and height as needed

    # sm.set_array([])
    # cbar = plt.colorbar(sm, cax=cbar_ax, orientation='vertical')
    # cbar_label = file_info[i*num_cols]["variable_name"].replace('_', ' ').title()  # Get the variable name for labeling
    # cbar.set_label(cbar_label, fontsize=8)
    # cbar.ax.tick_params(labelsize=5)  # Adjust the font size of the tick marks
    # cbar.ax.tick_params(labelsize=5)

sm.set_clim(vmin=minvalue, vmax=maxvalue)
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = plt.colorbar(sm, cax=cbar_ax)
cbar.set_label('SPEI Values on July 15')
    
# for ax in axes:
#     ax.images[-1].colorbar.remove()
for ax in axes:
    ax.images[-1].colorbar.remove()
    # ax.get_xaxis().get_major_formatter().set_scientific(False)
    # ax.get_yaxis().get_major_formatter().set_scientific(False)




plt.tight_layout()

# Show the plot
plt.show()
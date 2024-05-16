"""
purpose: map the downscaling for the 15th july (for the future data)
author: Luca Boestfleisch 
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


'the below code prints the days corresponding to july 15th of the years wanting to be plotted'
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

'define as needed'
num_rows = 2
num_cols = 5

fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 20))

axes = axes.flatten()

sm = plt.cm.ScalarMappable(cmap="bwr_r")
sm.set_array([])

minvalue = 2
maxvalue =-2

for i in range(num_rows):
    row_axes = axes[i*num_cols: (i+1)*num_cols]  

    min_val = np.inf
    max_val = -np.inf

    for j, source_info in enumerate(file_info[i*num_cols: (i+1)*num_cols]):
        directory = source_info["directory"]
        file = source_info["file"]
        variable_name = source_info["variable_name"]
        time_index = source_info['time']
        file_path = os.path.join(directory, file)

        'loading in the shape file of brandenburgs border'
        data = xr.open_dataset(file_path)
        shapefile_path = '' #adapt 
        gdf = gpd.read_file(shapefile_path)

        # Reproject the shapefile
        gdf_reprojected = gdf.to_crs(epsg=3034)
        output_shapefile_path = "" #adapt 
        gdf_reprojected.to_file(output_shapefile_path)
        gdf = gpd.read_file(output_shapefile_path)
        
        variable = data[variable_name].isel(time=int(time_index))
    
        ax = row_axes[j]
        variable.plot.imshow(x="lon", y='lat', ax=ax, cmap="bwr_r")
        gdf.plot(ax=ax, facecolor='none', edgecolor='black')
        ax.set_xlabel('Longitude', fontsize=6)
        ax.set_ylabel('Latitude', fontsize=6)
        ax.set_title("")
        ax.annotate('', xy=(0.95, 0.95), xycoords='axes fraction', xytext=(0.95, 0.85),
                    arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=2))
        ax.text(0.95, 0.95, 'N', transform=ax.transAxes, ha='center', va='center', fontsize=8,)
        ax.tick_params(axis='both', which='major', labelsize=5)  

        ax.xaxis.get_major_formatter().set_powerlimits((0, 1))  
        ax.yaxis.get_major_formatter().set_powerlimits((0, 1))  
        ax.xaxis.set_tick_params(labelsize=6)
        ax.yaxis.set_tick_params(labelsize=6)
        title = variable_name.replace("time = ", "")

    

sm.set_clim(vmin=minvalue, vmax=maxvalue)
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = plt.colorbar(sm, cax=cbar_ax)
cbar.set_label('SPEI Values on July 15')
    

for ax in axes:
    ax.images[-1].colorbar.remove()
    



plt.tight_layout()
plt.show()
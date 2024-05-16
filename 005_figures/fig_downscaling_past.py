"""
purpose: mapping the obsevational, past modelled, and downscaled past data 
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
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Times New Roman'

file_info = [
    {"directory": "C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT", "file": "obs_spei_avg_1970-2014.nc", "variable_name": "spei_avg"}, 
    {"directory": "C:/03_Capstone/Data/Future/historical/run2_140324", "file": "his_spei_avg_1970-2014.nc", "variable_name": "spei_avg"},  
    {"directory": "C:/03_Capstone/Data/Downscale/his-his", "file": "downscale_his_avg_110524.nc", "variable_name": "spei_avg"}, 


    {"directory": "C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT", "file": "obs_spei_1970-2014.nc", "variable_name": "spei", "time": "195"}, #1970
    {"directory": "C:/03_Capstone/Data/Future/historical/run2_140324", "file": "his_spei_1970-2014_obsgevpara.nc", "variable_name": "spei", "time": "195"}, #1970
    {"directory": "C:/03_Capstone/Data/Downscale/his-his", "file": "downscale_hismodel_110524_lr001_bs128_hs300_dp5_epoch200.nc", "variable_name": "predicted_spei", "time": "195"}, #1970


    {"directory": "C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT", "file": "obs_spei_1970-2014.nc", "variable_name": "spei", "time": "8231"}, #1992
    {"directory": "C:/03_Capstone/Data/Future/historical/run2_140324", "file": "his_spei_1970-2014_obsgevpara.nc", "variable_name": "spei", "time": "8231"}, #1992
    {"directory": "C:/03_Capstone/Data/Downscale/his-his", "file": "downscale_hismodel_110524_lr001_bs128_hs300_dp5_epoch200.nc", "variable_name": "predicted_spei", "time": "8231"}, #1992

    {"directory": "C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT", "file": "obs_spei_1970-2014.nc", "variable_name": "spei", "time": "16266"}, #2014
    {"directory": "C:/03_Capstone/Data/Future/historical/run2_140324", "file": "his_spei_1970-2014_obsgevpara.nc", "variable_name": "spei", "time": "16266"}, #1970
    {"directory": "C:/03_Capstone/Data/Downscale/his-his", "file": "downscale_hismodel_110524_lr001_bs128_hs300_dp5_epoch200.nc", "variable_name": "predicted_spei", "time": "16266"}, #1970

]

b = 0
for year in range (1970, 2014+1, 1):
    a = year - 1970
    if a == 0: 
        day = 195 #although it is the 196th day (July 15), python starts counting at 0, so it is the 195th day in python 
    elif ((a + 2)%4) == 0:  #+2 because 1972 is a leap year 
        day += 366
    else: 
        day += 365
    if year == 1970 or year == 1992 or year ==2014:
        print(f"year: {year}, day of July 25: {day}")    
    t = day 
    b += 1

num_rows = 4
num_cols = 3

fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 20))

axes = axes.flatten()

sm = plt.cm.ScalarMappable(cmap="bwr_r")
sm.set_array([])

minvalue = 3
maxvalue =-3

for i in range(num_rows):
    row_axes = axes[i*num_cols: (i+1)*num_cols]  # Axes for the current row
    for j in range(num_cols):  # Iterate over num_cols
        index = i * num_cols + j  # Calculate the index for file_info
        if index < len(file_info):  # Check if the index is within bounds
            source_info = file_info[index]  # Get the source info for the current index
            
            directory = source_info["directory"]
            file = source_info["file"]
            variable_name = source_info["variable_name"]
            file_path = os.path.join(directory, file)
            
            # Open the NetCDF dataset
            data = xr.open_dataset(file_path)
            
            # Get the variable
            if 'time' in source_info:  # Check if 'time' key exists in source_info
                time_index = int(source_info['time'])  # Convert to int
                variable = data[variable_name].isel(time=time_index)
            else:
                variable = data[variable_name]
            
            'import the Brandenburg shapefile '
            shapefile_path = 'C:/03_Capstone/Data/Analysis/shapefile_br/br_shapefile.shp'
            gdf = gpd.read_file(shapefile_path)

            gdf_reprojected = gdf.to_crs(epsg=3034)
            output_shapefile_path = "C:/03_Capstone/Data/Analysis/shapefile_br/br_shapefile_epsg3034.shp"
            gdf_reprojected.to_file(output_shapefile_path)
            gdf = gpd.read_file(output_shapefile_path)
            
            ax = row_axes[j]
            variable.plot.imshow(x="lon", y='lat', ax=ax, cmap="bwr_r")
            gdf.plot(ax=ax, facecolor='none', edgecolor='black')
            ax.set_xlabel('Longitude', fontsize=6)
            ax.set_ylabel('Latitude', fontsize=6)
            ax.set_title("")
            if i ==0: 
                ax.annotate('', xy=(0.95, 0.95), xycoords='axes fraction', xytext=(0.95, 0.85),
                            arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=2))
                ax.text(0.95, 0.95, 'N', transform=ax.transAxes, ha='center', va='center', fontsize=8,)
            ax.tick_params(axis='both', which='major', labelsize=5)  # Adjust the font size of the tick marks
            ax.xaxis.get_major_formatter().set_powerlimits((0, 1))  # Set the power limits for x-axis
            ax.yaxis.get_major_formatter().set_powerlimits((0, 1))  # Set the power limits for y-axis
            ax.xaxis.set_tick_params(labelsize=6)
            ax.yaxis.set_tick_params(labelsize=6)
            title = variable_name.replace("time = ", "")


   

sm.set_clim(vmin=minvalue, vmax=maxvalue)
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = plt.colorbar(sm, cax=cbar_ax)
cbar.set_label('SPEI Values')
    

for ax in axes:
    ax.images[-1].colorbar.remove()
   
plt.tight_layout()
plt.show()
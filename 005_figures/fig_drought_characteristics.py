"""
purpose: to map the Drought Characteristics (frequency, duration, intensity, and amount of flash droughts) 
adapt the fiel information as necessary
Date last updated: 20.04.2024
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
    {"directory": "C:/03_Capstone/Data/Analysis/01_drought_analysis/obs", "file": "obs_drought_analysis_190424.nc", "variable_name": "dr_freq"}, #observational, dr frequency
    {"directory": "C:/03_Capstone/Data/Analysis/01_drought_analysis/ssp126", "file": "ssp126_drought_analysis_190424.nc", "variable_name": "dr_freq"}, #ssp126, dr frequency
    {"directory": "C:/03_Capstone/Data/Analysis/01_drought_analysis/ssp585", "file": "ssp585_drought_analysis_190424.nc", "variable_name": "dr_freq"}, #ssp585, dr frequency 

    {"directory": "C:/03_Capstone/Data/Analysis/01_drought_analysis/obs", "file": "obs_avg_drought_duration_190424.nc", "variable_name": "avg_drought_duration"}, #observational, avg dr duration 
    {"directory": "C:/03_Capstone/Data/Analysis/01_drought_analysis/ssp126", "file": "ssp126_avg_drought_duration_190424.nc", "variable_name": "avg_drought_duration"}, #ssp126, avg dr duration 
    {"directory": "C:/03_Capstone/Data/Analysis/01_drought_analysis/ssp585", "file": "ssp585_avg_drought_duration_190424.nc", "variable_name": "avg_drought_duration"}, #ssp585, avg dr duration 

    {"directory": "C:/03_Capstone/Data/Analysis/01_drought_analysis/obs", "file": "obs_drought_analysis_190424.nc", "variable_name": "spei_min"}, #observational, dr intensity 
    {"directory": "C:/03_Capstone/Data/Analysis/01_drought_analysis/ssp126", "file": "ssp126_drought_analysis_190424.nc", "variable_name": "spei_min"}, #ssp126, dr intensity 
    {"directory": "C:/03_Capstone/Data/Analysis/01_drought_analysis/ssp585", "file": "ssp585_drought_analysis_190424.nc", "variable_name": "spei_min"}, #ssp585, dr intensity 

    {"directory": "C:/03_Capstone/Data/Analysis/01_drought_analysis/obs", "file": "obs_avg_drought_duration_190424.nc", "variable_name": "flash_dr_count"}, #observational, flash drought count 
    {"directory": "C:/03_Capstone/Data/Analysis/01_drought_analysis/ssp126", "file": "ssp126_avg_drought_duration_190424.nc", "variable_name": "flash_dr_count"}, #ssp126, flash drought count
    {"directory": "C:/03_Capstone/Data/Analysis/01_drought_analysis/ssp585", "file": "ssp585_avg_drought_duration_190424.nc", "variable_name": "flash_dr_count"}, #ssp585, flash drought count
]

time_index_past = 16435 - 1  #adapt 
time_index_future = 31411 - 1 #adapt 
num_rows = 4 #adapt 
num_cols = 3 #adapt 

fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 20))
plt.subplots_adjust(wspace=0, hspace=0.01) 
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05) 
axes = axes.flatten()



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
        file_path = os.path.join(directory, file)

        data = xr.open_dataset(file_path)
        shapefile_path = 'C:/03_Capstone/Data/Analysis/shapefile_br/br_shapefile.shp'
        gdf = gpd.read_file(shapefile_path)

        # Reproject the shapefile
        gdf_reprojected = gdf.to_crs(epsg=3034)
        output_shapefile_path = "C:/03_Capstone/Data/Analysis/shapefile_br/br_shapefile_epsg3034.shp"
        gdf_reprojected.to_file(output_shapefile_path)
        gdf = gpd.read_file(output_shapefile_path)
        
        # Extract the variable
        if "time" in data.dims: 
            if "obs" in directory: 
                variable = data[variable_name].isel(time=time_index_past)

            else: 
                variable = data[variable_name].isel(time=time_index_future)
                # title = variable_name.replace("time =", "")
            
        else: 
            variable = data[variable_name]
            # title = variable_name.replace("time =", "")

        # Plot the variable
        ax = row_axes[j]
        if i == 0: 
            maxvalue = 200
            minvalue = 0
            variable.plot.imshow(x="lon", y='lat', ax=ax, vmin = minvalue, vmax=maxvalue, cmap="RdYlGn_r")
            sm = plt.cm.ScalarMappable(cmap="RdYlGn_r")
            sm.set_clim(vmin=minvalue, vmax=maxvalue)

        
        if i == 1: 
            maxvalue = 50
            minvalue = 0
            variable.plot.imshow(x="lon", y='lat', ax=ax, vmin = minvalue, vmax=maxvalue, cmap="RdYlGn_r")
            sm = plt.cm.ScalarMappable(cmap="RdYlGn_r")
            sm.set_clim(vmin=minvalue, vmax=maxvalue)
            
        if i == 2: 
            maxvalue = -1.5
            minvalue = -4.5
            variable.plot.imshow(x="lon", y='lat', ax=ax, vmin=minvalue, vmax=maxvalue, cmap="RdYlGn")
            sm = plt.cm.ScalarMappable(cmap="RdYlGn")
            sm.set_clim(vmin=minvalue, vmax=maxvalue)
        
        if i == 3: 
            maxvalue = 120
            minvalue = 0
            variable.plot.imshow(x="lon", y='lat', ax=ax, vmin = minvalue, vmax=maxvalue, cmap="RdYlGn_r")
            sm = plt.cm.ScalarMappable(cmap="RdYlGn_r")
            sm.set_clim(vmin=minvalue, vmax=maxvalue)
        # else: 
        #     variable.plot.imshow(x="lon", y='lat', ax=ax, cmap="RdYlGn_r")

        gdf.plot(ax=ax, facecolor='none', edgecolor='black')
        ax.set_xlabel('Longitude', fontsize=6)
        ax.set_ylabel('Latitude', fontsize=6)
        ax.set_title("")

        if j == 0 and i == 0:
            ax.annotate('', xy=(0.95, 0.95), xycoords='axes fraction', xytext=(0.95, 0.85),
                        arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=2))
            ax.text(0.95, 0.95, 'N', transform=ax.transAxes, ha='center', va='center', fontsize=8,)
        
        ax.tick_params(axis='both', which='major', labelsize=5)  # Adjust the font size of the tick marks

        ax.xaxis.get_major_formatter().set_powerlimits((0, 1))  # Set the power limits for x-axis
        ax.yaxis.get_major_formatter().set_powerlimits((0, 1))  # Set the power limits for y-axis
        ax.xaxis.set_tick_params(labelsize=6)
        ax.yaxis.set_tick_params(labelsize=6)
        title = variable_name.replace("time = ", "")

    
    cbar_ax = fig.add_axes([0.95, 0.8 - i*0.2, 0.02, 0.15])  # Adjust position and height as needed

    
    
    sm.set_array([])
    cbar = plt.colorbar(sm, cax=cbar_ax, orientation='vertical')
    cbar_label = file_info[i*num_cols]["variable_name"].replace('_', ' ').title()  # Get the variable name for labeling
    cbar.set_label(cbar_label, fontsize=8)
    cbar.ax.tick_params(labelsize=5)  # Adjust the font size of the tick marks
    cbar.ax.tick_params(labelsize=5)  # Adjust the font size of the color bar tick marks
    
    
    variable_name = source_info["variable_name"]
    # Use regular expression to remove numeric values and extra characters
    title = re.sub(r'[^a-zA-Z\s]', '', variable_name)
    title = title.replace("time =", "")
 


for ax in axes:
    ax.images[-1].colorbar.remove()




plt.tight_layout()
plt.show()
"trying 8 with dif sources"
import os
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import pyproj
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mpl


mpl.rcParams['font.family'] = 'Times New Roman'

# C:\03_Capstone\Data\Analysis\avg_july
# Define file information for each source
"File information for Avg"
file_info = [
    {"directory": "C:/03_Capstone/Data/Analysis/avg_2015-2100", "file": "ssp126_anomaly_avg_2015-2035.nc", "variable_name": "spei_anomaly"},
    {"directory": "C:/03_Capstone/Data/Analysis/avg_2015-2100", "file": "ssp126_anomaly_avg_2035-2055.nc", "variable_name": "spei_anomaly"},
    {"directory": "C:/03_Capstone/Data/Analysis/avg_2015-2100", "file": "ssp126_anomaly_avg_2055-2075.nc", "variable_name": "spei_anomaly"},
    {"directory": "C:/03_Capstone/Data/Analysis/avg_2015-2100", "file": "ssp126_anomaly_avg_2075-2100.nc", "variable_name": "spei_anomaly"},#end of ssp126 mean 

    {"directory": "C:/03_Capstone/Data/Analysis/avg_2015-2100", "file": "ssp585_anomaly_avg_2015-2035.nc", "variable_name": "spei_anomaly"},
    {"directory": "C:/03_Capstone/Data/Analysis/avg_2015-2100", "file": "ssp585_anomaly_avg_2035-2055.nc", "variable_name": "spei_anomaly"},
    {"directory": "C:/03_Capstone/Data/Analysis/avg_2015-2100", "file": "ssp585_anomaly_avg_2055-2075.nc", "variable_name": "spei_anomaly"},
    {"directory": "C:/03_Capstone/Data/Analysis/avg_2015-2100", "file": "ssp585_anomaly_avg_2075-2100.nc", "variable_name": "spei_anomaly"}, #end of ssp585 mean 
]
"File information for Per1"
# file_info = [
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp126_anomaly_per1_2015-2035.nc", "variable_name": "spei_anomaly"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp126_anomaly_per1_2035-2055.nc", "variable_name": "spei_anomaly"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp126_anomaly_per1_2055-2075.nc", "variable_name": "spei_anomaly"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp126_anomaly_per1_2075-2100.nc", "variable_name": "spei_anomaly"},#end of ssp126 mean 

#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp585_anomaly_per1_2015-2035.nc", "variable_name": "spei_anomaly"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp585_anomaly_per1_2035-2055.nc", "variable_name": "spei_anomaly"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp585_anomaly_per1_2055-2075.nc", "variable_name": "spei_anomaly"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp585_anomaly_per1_2075-2100.nc", "variable_name": "spei_anomaly"}, #end of ssp585 mean 

# ]
"file information for DOWNSCALE figure"
# file_info = [
#     {"directory": "C:/03_Capstone/Data/Downscale/ssp126/anomaly_mean", "file": "ssp126_downscale_050524_avg_2015-2100.nc", "variable_name": "spei_avg"},
#     {"directory": "C:/03_Capstone/Data/Analysis/avg_2015-2100", "file": "ssp126_avg_2015-2100.nc", "variable_name": "spei_avg"},
#     {"directory": "C:/03_Capstone/Data/Downscale/ssp585/anomaly_mean", "file": "downscale_050524_ssp585_avg_2015-2100.nc", "variable_name": "spei_avg"},
#     {"directory": "C:/03_Capstone/Data/Analysis/avg_2015-2100", "file": "ssp585_avg_2015-2100.nc", "variable_name": "spei_avg"},#end of ssp126 mean 

#     {"directory": "C:/03_Capstone/Data/Downscale/ssp126/ssp126_downscale_per1", "file": "ssp126_downscale_050524_per1_2015-2100.nc", "variable_name": "spei_per1"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp126_per1_2015-2100.nc", "variable_name": "spei_per1"},
#     {"directory": "C:/03_Capstone/Data/Downscale/ssp585/ssp585_downscale_per1", "file": "ssp585_downscale_050524_per1_2015-2100.nc", "variable_name": "spei_per1"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp585_per1_2015-2100.nc", "variable_name": "spei_per1"}, #end of ssp585 mean 

# ]

"file information for absolute avg, not downscaled"
# file_info = [
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp126_per1_2015-2035.nc", "variable_name": "spei_per1"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp126_per1_2035-2055.nc", "variable_name": "spei_per1"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp126_per1_2055-2075.nc", "variable_name": "spei_per1"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp126_per1_2075-2100.nc", "variable_name": "spei_per1"},#end of ssp126 mean 

#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp585_per1_2015-2035.nc", "variable_name": "spei_per1"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp585_per1_2035-2055.nc", "variable_name": "spei_per1"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp585_per1_2055-2075.nc", "variable_name": "spei_per1"},
#     {"directory": "C:/03_Capstone/Data/Analysis/per1_2015-2100", "file": "ssp585_per1_2075-2100.nc", "variable_name": "spei_per1"}, #end of ssp585 mean 
# ]

# Define the number of rows and columns for subplots
num_rows = 2
num_cols = 4

# Create the figure and axes
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 10))

# Flatten the axes array for easier iteration
axes = axes.flatten()
# norm = plt.Normalize(-1, 1)
sm = plt.cm.ScalarMappable(cmap="seismic_r") #OrRd_r or seismic_r
sm.set_array([])  # Dummy array needed for ScalarMappable

minvalue = 1
maxvalue =-1

# Iterate over each source
for i, source_info in enumerate(file_info):
    # File information
    directory = source_info["directory"]
    file = source_info["file"]
    variable_name = source_info["variable_name"]
    file_path = os.path.join(directory, file)
    
    # Open the NetCDF dataset
    data = xr.open_dataset(file_path)
    
    # Get the title from the filename
    title = os.path.splitext(file)[0]
    
    # Import the shape file 
    shapefile_path = 'C:/03_Capstone/Data/Analysis/shapefile_br/br_shapefile.shp'
    gdf = gpd.read_file(shapefile_path)

    # Reproject the shapefile
    gdf_reprojected = gdf.to_crs(epsg=3034)
    output_shapefile_path = "C:/03_Capstone/Data/Analysis/shapefile_br/br_shapefile_epsg3034.shp"
    gdf_reprojected.to_file(output_shapefile_path)
    gdf = gpd.read_file(output_shapefile_path)

    # Extract the variable
    variable = data[variable_name]

    # Plot the variable
    ax = axes[i]
    variable.plot.imshow(x="lon", y='lat', ax=ax, vmin=minvalue, vmax=maxvalue, cmap="seismic_r") #OrRd_r or seismic_r
    gdf.plot(ax=ax, facecolor='none', edgecolor='black')
    # ax.set_title(title, fontsize=8)
    ax.set_xlabel('Longitude', fontsize=8)
    ax.set_ylabel('Latitude', fontsize=8)
    if i == 0:  
        ax.annotate('', xy=(0.95, 0.95), xycoords='axes fraction', xytext=(0.95, 0.85),
                arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=2))
        ax.text(0.95, 0.95, 'N', transform=ax.transAxes, ha='center', va='center', fontsize=8,)

    
   
    

    
# Add a common colorbar
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])  # Adjust position as needed
# norm = plt.Normalize(-1, 1)
sm = plt.cm.ScalarMappable(cmap="seismic_r") #OrRd_r or seismic_r
sm.set_array([])
sm.set_clim(vmin=minvalue, vmax=maxvalue)
cbar = plt.colorbar(sm, cax=cbar_ax)
cbar.set_label('SPEI Anomaly')


for ax in axes:
    ax.images[-1].colorbar.remove()

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()
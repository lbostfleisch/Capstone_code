import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import xarray as xr

file_info = [
    {"directory": "C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT", "file": "obs_spei_1970-2014.nc", "variable_name": "spei"},
    {"directory": "C:/03_Capstone/Data/Future/historical/run2_140324", "file": "his_spei_1970-2014_obsgevpara.nc", "variable_name": "spei"},
    {"directory": "C:/03_Capstone/Data/Future/ssp126/run1_200324", "file": "ssp126_spei_2015-2100_obsgevpara.nc", "variable_name": "spei"},
    {"directory": "C:/03_Capstone/Data/Future/ssp585/02_run2_160324", "file": "ssp585_spei_2015-2100_obsgevpara.nc", "variable_name": "spei"},
]

num_rows = 2
num_cols = 2

fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 10))
axes = axes.flatten()

minvalue = -5
maxvalue = 2

for i, source_info in enumerate(file_info):
    # File information
    directory = source_info["directory"]
    file = source_info["file"]
    variable_name = source_info["variable_name"]
    file_path = os.path.join(directory, file)
    # Open the NetCDF dataset
    data = xr.open_dataset(file_path)
    time = data.variables["time"][:]

    # Get the title from the filename
    title = os.path.splitext(file)[0]

    # Extract the variable
    variable = data[variable_name]
    variable_to_average = data.variables[variable_name][:] 

    average_values = np.nanmean(variable_to_average, axis=(1, 2))
    average_values = np.percentile(variable_to_average, 99, axis = (1,2))

    ax = axes[i]  # Get the current subplot
    ax.plot(time, average_values, label='Mean Value', color='lightblue')  # Plot the average
    ax.set_xlabel('Time (days)')
    ax.set_ylabel(f'Mean {variable_name} Value')
    ax.set_ylim(minvalue, maxvalue)

    slope, intercept, _, _, _ = stats.linregress(time, average_values)
    trend_line = slope * time + intercept
    ax.plot(time, trend_line, color='red', linestyle='--')
    ax.text(0.05, 0.05, f'Slope: {slope:.10f}', transform=ax.transAxes, color='black', fontsize=10)
    
    # ax.set_title(title, fontsize=8)

    # ax.legend(loc="lower left")
    ax.legend().set_visible(False)

plt.tight_layout()
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0), ncol=2)
# Show the plot
plt.show()

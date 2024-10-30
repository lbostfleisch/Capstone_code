"""
23.1.24
trying to plot 
works to plot, but it is weird with the rotated coordinates 
"""
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

file_path = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/rotated_files/231024_reprojection_pr_original_theta_phi.nc'  # Replace with the path to your NetCDF file
# file_path = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/original_files/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19660101-19701231.nc'
# file_path = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/output/spei_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_1966-2005.nc'
dataset = nc.Dataset(file_path)

print("Variables and their dimensions:")
for var_name in dataset.variables.keys():
    var = dataset.variables[var_name]
    print(f"Variable: {var_name}, Dimensions: {var.dimensions}, Shape: {var.shape}")


# Inspect the dataset variables
print("Variables in the dataset:", dataset.variables.keys())

# Extract time, lat, lon, and the data variable
time = dataset.variables['time'][:]  # Time variable
lat = dataset.variables['lat'][:]    # Latitude variable
lon = dataset.variables['lon'][:]    # Longitude variable

# Replace 'your_variable_name' with the actual variable name
data = dataset.variables['pr']  # Data variable (no slicing yet)

# Check the shape of the data
print(f"Data shape: {data.shape}")

# Select a specific time step (e.g., first time step)
time_step = 0
data_at_time = data[time_step, :, :]  # Slicing for the first time step

# Plot the data for the selected time step
plt.figure(figsize=(10, 6))
plt.contourf(lon, lat, data_at_time, cmap='viridis')
plt.colorbar(label='Data Value')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title(f'Data at Time = {time_step}')

# Show the plot
plt.show()

# Close the dataset
dataset.close()
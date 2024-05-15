"""
file to calculate the min and max of avg/per1 anomalies
on the 09.05.2024: added that it also creates a new file with from the max 
"""

from netCDF4 import Dataset
import numpy as np

lon_max = 4323286.0
lon_min =  4028021.5  
lat_max = 3023612.5
lat_min = 2641848.5

input_file = "C:/03_Capstone/Data/Analysis/01_drought_analysis/ssp585/ssp585_drought_analysis_190424.nc"
# C:\03_Capstone\Data\Python_NetCDF_join\Output\run3_140324_CURRENT
data = Dataset(input_file, 'r')
var = "spei_min"      #flash_dr_count, avg_drought_duration, dr_freq, spei_min
lon = data.variables["lon"][:]
lat = data.variables['lat'][:]
# time = data.variables['time'][:]
# time = data.variables['time'][:]


"just calculating the min and max"
max_value = float('-inf') 
min_value = float('inf')

# for t in range(len(time)):
# for j in range(len(lon)):
#     for i in range(len(lat)):
        
#         data_input = data.variables[var][j, i]
#         if data_input > max_value: 
#             max_value = data_input
#         if data_input < min_value: 
#             min_value = data_input

"drought frequency, spei_min"
data_slice = data.variables[var][:, :, :]
filtered_data = data_slice[np.isfinite(data_slice)]
max_value = np.max(filtered_data)
min_value = np.min(filtered_data)


print("Min.:", min_value)
print("Max.:", max_value)


"creating a new netcdf with the max temperature"

# array = np.zeros((len(lon), len(lat)))


# for j in range(len(lon)):
#     for i in range(len(lat)): 
#         max_value = float('-inf')
#         for t in range(len(time)): 
#             data_input = data.variables[var][t,j,i]
#             if data_input > max_value: 
#                 max_value = data_input
#                 array[j,i] = max_value
#         print("lon", j, "lat:", i, "max_value:", max_value)

# output_file = "C:/03_Capstone/Data/Python_NetCDF_join/DWD CDC/Tmax_nc/Output/max_tasmax_1970-2014.nc"

# with Dataset(output_file, 'w', format='NETCDF4') as ds:
#     # time = ds.createDimension('time', len(time))
#     lon = ds.createDimension('lon', len(lon))  
#     lat = ds.createDimension('lat', len(lat))  

#     # times = ds.createVariable('time', 'f4', ('time',))
#     lons = ds.createVariable('lon', 'f4', ('lon',))  
#     lats = ds.createVariable('lat', 'f4', ('lat',)) 
#     value = ds.createVariable(var, 'f4', ('lon', 'lat'))  

#     value.units = 'Unknown'

#     lons[:] = np.linspace(lon_min, lon_max, len(lon))
#     lats[:] = np.linspace(lat_min, lat_max, len(lat))
#     # times[:] = np.arange(0, len(time), 1)

#     value[:, :] = array            


"removing values ==0 "

# input_withnan = "C:/03_Capstone/Data/Python_NetCDF_join/DWD CDC/Tmax_nc/Output/max_tasmax_1970-2014.nc"
# data_withnan = Dataset(input_withnan, 'r')

# input_file = "C:/03_Capstone/Data/Python_NetCDF_join/DWD CDC/Tmax_nc/Output/max_tasmax_1970-2014.nc"
# output_file = "C:/03_Capstone/Data/Python_NetCDF_join/DWD CDC/Tmax_nc/Output/max_tasmax_1970-2014_no0.nc"

# # Open the input NetCDF file
# with Dataset(input_file, 'r') as data:
#     # Assuming 'var' is the variable you want to process
#     var = "tasmax"  # Replace "your_variable_name" with the actual variable name
    
#     # Read the data
#     data_array = data.variables[var][:]

#     # Create a mask where the values are not equal to 0
#     mask = data_array != 0

#     # Apply the mask to remove the values equal to 0
#     data_array[mask == False] = np.nan

#     # Create a new NetCDF file
#     with Dataset(output_file, "w") as output_dataset:
#         # Create dimensions for the output dataset (assuming lon and lat are the dimensions)
#         output_dataset.createDimension("lon", len(data.dimensions["lon"]))
#         output_dataset.createDimension("lat", len(data.dimensions["lat"]))

#         # Create variables in the output dataset
#         lon_variable = output_dataset.createVariable("lon", data.variables["lon"].dtype, ("lon",))
#         lat_variable = output_dataset.createVariable("lat", data.variables["lat"].dtype, ("lat",))
#         data_variable = output_dataset.createVariable(var, data.variables[var].dtype, ("lon", "lat"))

#         # Assign values to the variables
#         lon_variable[:] = data.variables["lon"][:]
#         lat_variable[:] = data.variables["lat"][:]
#         data_variable[:] = data_array
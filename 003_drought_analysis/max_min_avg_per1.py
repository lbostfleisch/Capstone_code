"""
purpose: calculate the min and max of the avergae/top 1% SPEI files. Also creates a new file from the output. 
Author: Luca Boestfleisch
Date: 09.05.2024
"""

from netCDF4 import Dataset
import numpy as np

lon_max = 4323286.0
lon_min =  4028021.5  
lat_max = 3023612.5
lat_min = 2641848.5

input_file = "C:/03_Capstone/a_publishing/data/complete_CMIP5_EUR-11_DMI_ICHEC-EC-EARTH_historical_HIRHAM5/r12i1p1_v1/output/spei_CMIP5_EUR-11_DMI_ICHEC-EC-EARTH_historical_HIRHAM5_r12i1p1_v1_day.nc" #adapt
data = Dataset(input_file, 'r')
var = "spei"      ##adapt
lon = data.variables["rlon"][:]
lat = data.variables['rlat'][:]
"uncomment below if there is a time dimension"
time = data.variables['time'][:]


"just calculating the min and max"
# max_value = float('-inf') 
# min_value = float('inf')


# for t in range(len(time)): #uncomment this line if there is a time dimension
#     for j in range(len(lon)):
#         for i in range(len(lat)):
            
#             data_input = data.variables[var][t, j, i]
#             if data_input > max_value: 
#                 max_value = data_input
#             if data_input < min_value: 
#                 min_value = data_input

# "drought frequency, spei_min"
# data_slice = data.variables[var][:, :, :]
# filtered_data = data_slice[np.isfinite(data_slice)]
# max_value = np.max(filtered_data)
# min_value = np.min(filtered_data)


# print("Min.:", min_value)
# print("Max.:", max_value)


"creating a new netcdf with the max temperature"

array = np.zeros((len(lon), len(lat)))


for j in range(len(lon)):
    for i in range(len(lat)): 
        max_value = float('-inf')
        for t in range(len(time)): 
            data_input = data.variables[var][t,j,i]
            if data_input > max_value: 
                max_value = data_input
                array[j,i] = max_value
        print("lon", j, "lat:", i, "max_value:", max_value)

output_file = "C:/03_Capstone/a_publishing/data/complete_CMIP5_EUR-11_DMI_ICHEC-EC-EARTH_historical_HIRHAM5/r12i1p1_v1/output/analysis/speimin_CMIP5_EUR-11_DMI_ICHEC-EC-EARTH_historical_HIRHAM5_r12i1p1_v1_day.nc" #adapt

with Dataset(output_file, 'w', format='NETCDF4') as ds:
    # time = ds.createDimension('time', len(time))
    lon = ds.createDimension('rlon', len(lon))  
    lat = ds.createDimension('rlat', len(lat))  

    # times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('rlon', 'f4', ('rlon',))  
    lats = ds.createVariable('rlat', 'f4', ('rlat',)) 
    value = ds.createVariable(var, 'f4', ('rlon', 'rlat'))  

    value.units = 'Unknown'

    lons[:] = np.linspace(lon_min, lon_max, len(lon))
    lats[:] = np.linspace(lat_min, lat_max, len(lat))
    # times[:] = np.arange(0, len(time), 1)

    value[:, :] = array            



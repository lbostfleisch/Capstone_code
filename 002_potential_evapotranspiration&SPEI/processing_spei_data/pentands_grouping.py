"""
File for grouping the days into pentads (5 days)
working on the CMIP5 data 
goal: to compare the CMIP5 data with the observational data for every 5 days 
"""
from netCDF4 import Dataset
import os
import numpy as np
import netCDF4 as nc

# file_name = "spei_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_1966-2005.nc"
# file_path = os.path.join("C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/output", file_name)
# spei_data = Dataset(file_path, 'r')
# lon = spei_data.variables['rlon'][:]
# lat = spei_data.variables['rlat'][:]
# time = spei_data.variables['time'][:]

"trying with the observational data"
file_name = "obs_spei_1970-2014.nc"
file_path = os.path.join("C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT/", file_name)
spei_data = Dataset(file_path, 'r')

lon = spei_data.variables['lon'][:]
lat = spei_data.variables['lat'][:]
time = spei_data.variables['time'][:]

"For the CMIP5 data"
# lat_min, lat_max = -6.0, 8.0
# lon_min, lon_max = -8.0, -1.0
# lon_length = 63
# lat_length = 128

"For the CMIP6 and observational data"
lon_max, lon_min = 4323286.0, 4028021.5
lat_max, lat_min = 3023612.5, 2641848.5
lon_length = 10
lat_length = 7

"have the first pentad starting on the 1970, so first need to crop the dataset of the past modelled data from starting point 1966 to 1970"
# start_day_CMIP5 = 4 * 365 + 1 #because it is 4 years in, and one leap year in the time frame
# end_day_CMIP5 = len(time)
# all_days = end_day_CMIP5 - start_day_CMIP5
# num_pentads = all_days // 5

"for the past CMIP6 and observational"
len_days = 16435 
end_day_sub = (9 * 365 + 2) #because the observational data set goes until 2014 (not 2004)
all_days = len_days - end_day_sub
num_pentads = all_days // 5 

# maybe making list with the stored days and their corresponding pentad 

Array_pentad = np.zeros((num_pentads, lon_length, lat_length), dtype=np.float32)  
pentad_indices = np.zeros(all_days, dtype=np.int32)

for j in range(lon_length):
    for i in range(lat_length):
        for p in range(num_pentads):
            start_pentad = p * 5
            end_pentad = start_pentad + 5

            spei_var = spei_data.variables['spei'][start_pentad:end_pentad, j, i] #check if the 
            print(spei_var)
            Array_pentad[p, j, i] = np.mean(spei_var)

            pentad_indices[start_pentad:end_pentad] = p
        print(f'lon: {j}, lat: {i}')


# output_directory = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/output"
# output_file = "pentads_spei_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_1966-2005.nc"

"observational data"
output_directory = "C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT/"
output_file = "pentads_obs_spei_1970-2014.nc"

# with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
#     pentad = ds.createDimension('pentad', num_pentads)
#     lon = ds.createDimension('rlon', lon_length)  
#     lat = ds.createDimension('rlat', lat_length)  

#     pentads = ds.createVariable('pentad', 'f4', ('pentad',))
#     lons = ds.createVariable('rlon', 'f4', ('rlon',))  
#     lats = ds.createVariable('rlat', 'f4', ('rlat',)) 
#     pentad_avg = ds.createVariable('pentad_avg', 'f4', ('pentad', 'rlon', 'rlat'))  

#     pentad_avg.units = 'Unknown'

#     lons[:] = np.linspace(lon_min, lon_max, lon_length)
#     lats[:] = np.linspace(lat_min, lat_max,lat_length)
#     pentads[:] = np.arange(0, num_pentads, 1)

#     pentad_avg[:, :, :] = Array_pentad

with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
    pentad = ds.createDimension('pentad', num_pentads)
    lon = ds.createDimension('lon', lon_length)  
    lat = ds.createDimension('lat', lat_length)  

    pentads = ds.createVariable('pentad', 'f4', ('pentad',))
    lons = ds.createVariable('lon', 'f4', ('rlon',))  
    lats = ds.createVariable('lat', 'f4', ('rlat',)) 
    pentad_avg = ds.createVariable('pentad_avg', 'f4', ('pentad', 'lon', 'lat'))  

    pentad_avg.units = 'Unknown'

    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max,lat_length)
    pentads[:] = np.arange(0, num_pentads, 1)

    pentad_avg[:, :, :] = Array_pentad

print("calculated the avg spei per pentad")

ds_out = Dataset(os.path.join(output_directory, output_file), 'r')
print("Dimensions in the output file:")
for dim_name, dimension in ds_out.dimensions.items():
    print(f"{dim_name}: {len(dimension)}")

print("Dimensions in the input file:")
for dim_name, dimension in spei_data.dimensions.items():
    print(f"{dim_name}: {len(dimension)}")

ds_out.close()
spei_data.close()



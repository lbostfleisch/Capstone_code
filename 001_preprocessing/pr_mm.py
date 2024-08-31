""""
purpose: converting the precipitation files from kg/m2/s (format given on the esgf website) to mm 
Author: Luca Boestfleisch 
last accessed: 29.02.2024

note: the comment 'adapt' requires specifying a filepath or similar 

"""
import xarray as xr
import matplotlib.pyplot as plt
import os
from netCDF4 import Dataset
import numpy as np

pr_file = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_DMI_ICHEC-EC-EARTH_historical_HIRHAM5/r12i1p1_v1/pr/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_DMI-HIRHAM5_v1_day_joined.nc"  #adapt
pr_data = Dataset(pr_file, 'r')
all_days = 14610
#14610 past CMIP5 
#16435 past CMIP6
#31411 future 
var = "pr" #adapt

"CMIP 6"
# lon_max = 4323286.0
# lon_min =  4028021.5  
# lat_max = 3023612.5
# lat_min = 2641848.5
# lon_length = 10
# lat_length = 7

"CMIP 5"
lat_min, lat_max = -6.0, 8.0
lon_min, lon_max = -8.0, -1.0
lon_length = 63
lat_length = 128

lon = pr_data.variables['rlon'][:]
lat = pr_data.variables['rlat'][:]
time = pr_data.variables['time'][:]
nt, nlons, nlats = len(time), len(lon), len(lat)
Array = np.zeros((all_days, lon_length, lat_length), dtype=np.float32)  

water_density = 1000  # kg/m^3

# Convert precipitation to mm/day

for t in range(all_days):  
    for j in range(len(lon)):
        for i in range(len(lat)):
            pr_var = pr_data.variables[var][t, j, i] 
            
            "converting the precipitation values from kg/m2/s to mm"
            pr = pr_var * 1000 / water_density *(60*60*24)
            Array[t, j, i] = pr
    print(f"Pr, Time step: {t}/{all_days}")


"""Create a new netCDF file"""
output_directory = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_DMI_ICHEC-EC-EARTH_historical_HIRHAM5/r12i1p1_v1/pr/" #adapt
output_file = "pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_DMI-HIRHAM5_v1_day_joined_mm.nc" #adapt

with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days)
    lon = ds.createDimension('rlon', lon_length)  #### ISSUE HERE 
    lat = ds.createDimension('rlat', lat_length) ### ISSUE HERE 

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('rlon', 'f4', ('rlon',))  # Corrected variable name
    lats = ds.createVariable('rlat', 'f4', ('rlat',))  # Corrected variable name
    value = ds.createVariable(var, 'f4', ('time', 'rlon', 'rlat'))  # Corrected variable names

    value.units = 'Unknown'

    # Use the specified boundaries for lons and lats
    lons[:] = np.linspace(lon_min, lon_max, lon_length)   #longitude should be 10- 15
    lats[:] = np.linspace(lat_min, lat_max, lat_length)   #latitude should be 51-54
    times[:] = np.arange(0, all_days, 1)

    value[:, :, :] = Array
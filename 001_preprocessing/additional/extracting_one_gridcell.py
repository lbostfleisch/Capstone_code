"""
File to extract 1 grid cell from a netcdf file 
11.10.24
"""
import xarray as xr 
import matplotlib.pyplot as plt

file_path = "C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT/obs_spei_1970-2014.nc"
ds = xr.open_dataset(file_path)

min_lon = ds['lon'].isel(lon=0).values
print(min_lon)
min_lat = ds['lat'].isel(lat=0).values
print(min_lat)
variable_name = 'spei'

#checking the available lon/lat
print("Available latitude values:", ds['lat'].values)
print("Available longitude values:", ds['lon'].values)

lon_value = 4033112.2
lat_value = 2646871.8

variable_data = ds[variable_name]
one_grid_cell = variable_data.sel(lat=lat_value, lon=lon_value, method='nearest')


output_file_path = 'C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT/one_grid_cell_obs_spei_1970-2014.nc'

one_grid_cell.to_dataset(name='spei').to_netcdf(output_file_path)


ds = xr.open_dataset(output_file_path)


variable_name = "spei" 
data = ds[variable_name]
print(data.dims)
print(data.values)

print("created new netcdf file with one grid cell")
data.plot()
plt.title(f"{variable_name} for one grid cell")
plt.ylabel(f"{variable_name}")
plt.xlabel("Time")


plt.show()

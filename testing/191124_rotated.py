"""
rotation file 12.11.24
"""
import numpy as np
import netCDF4 as nc
from cordex.grid import rotated_grid_transform
from netCDF4 import Dataset


#parameteres from the cordex website: https://cordex.org/domains/cordex-region-euro-cordex/
rot_pole_lat = 198
rot_pole_lon = 39.25
TLC_lat = 331.79
TLC_lon = 21.67
# Nx = 106
# Ny = 103
Nx = 424
Ny = 412

all_days = 1826

input_file_path = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/original_files/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19660101-19701231.nc'  # Replace with your actual file path
output_file_path = 'C:/03_Capstone/a_publishing/data/test_files_rot/1911_type5_test_rot.nc'


# with nc.Dataset(input_file_path) as dataset:
#     # Read rotated coordinates and variable
#     rlon = dataset.variables['rlon'][:]
#     rlat = dataset.variables['rlat'][:]
#     pr_data = dataset.variables['pr'][:]  # Precipitation data (time, rlat, rlon)

#     # Convert rotated grid to geographic coordinates
#     lon_geo, lat_geo = rotated_grid_transform(
#         lon_arr=np.meshgrid(rlon, rlat)[0],
#         lat_arr=np.meshgrid(rlon, rlat)[1],
#         np_lon=rot_pole_lon,
#         np_lat=rot_pole_lat,
#         direction="rot2geo"
#     )

#     # Ensure the output grid dimensions match (Ny, Nx)
#     lon_geo = lon_geo[:Ny, :Nx]
#     lat_geo = lat_geo[:Ny, :Nx]

# # Initialize the output data array
# output_data = np.zeros((all_days, Ny, Nx), dtype=np.float32)

# # Fill the output array (slice the input data to match dimensions)
# output_data[:, :, :] = pr_data[:all_days, :Ny, :Nx]

# # Write to the new NetCDF file
# with Dataset(output_file_path, 'w', format='NETCDF4') as ds:
#     # Define dimensions
#     ds.createDimension('time', all_days)
#     ds.createDimension('lon', Nx)
#     ds.createDimension('lat', Ny)

#     # Create variables
#     times = ds.createVariable('time', 'f4', ('time',))
#     lons = ds.createVariable('lon', 'f4', ('lon',))
#     lats = ds.createVariable('lat', 'f4', ('lat',))
#     pr = ds.createVariable('pr', 'f4', ('time', 'lat', 'lon'), zlib=True)

#     # Add metadata
#     ds.description = 'Non-rotated coordinate precipitation data'
#     ds.source = 'Converted from rotated grid using Python'
#     pr.units = 'mm/day'  # Example, adjust to actual units

#     # Assign values
#     times[:] = np.arange(0, all_days)
#     lons[:] = lon_geo[0, :]
#     lats[:] = lat_geo[:, 0]
#     pr[:, :, :] = output_data

# print("Conversion completed. Output saved to:", output_file_path)


"2nd approach with TLC: not working"
# with nc.Dataset(input_file_path) as dataset:
#     # Read rotated coordinates and variable
#     print("Dimensions of the input file:")
#     for dim_name, dim in dataset.dimensions.items():
#         print(f"  {dim_name}: {len(dim)}")
        
#     rlon = dataset.variables['rlon'][:]  # Rotated longitude
#     rlat = dataset.variables['rlat'][:]  # Rotated latitude
#     pr_data = dataset.variables['pr'][:]  # Precipitation data (time, rlat, rlon)

#     # Create 2D rotated coordinate grids
#     rlon_2d, rlat_2d = np.meshgrid(rlon, rlat)

#     # Convert rotated grid to geographic coordinates using the CORDEX transformation
#     lon_geo, lat_geo = rotated_grid_transform(
#         lon_arr=rlon_2d,
#         lat_arr=rlat_2d,
#         np_lon=rot_pole_lon,
#         np_lat=rot_pole_lat,
#         direction="rot2geo"
#     )

#     # Adjust the transformed grid to start at TLC (Top-Left Corner geographic coordinates)
#     # lon_geo = lon_geo - lon_geo[0, 0] + TLC_lon
#     # lat_geo = lat_geo - lat_geo[0, 0] + TLC_lat

#     # Ensure the output grid dimensions match (Ny, Nx)
#     lon_geo = lon_geo[:Ny, :Nx]
#     lat_geo = lat_geo[:Ny, :Nx]

# # Initialize the output data array
# output_data = np.zeros((all_days, Ny, Nx), dtype=np.float32)

# # Fill the output array (slice the input data to match dimensions)
# output_data[:, :, :] = pr_data[:all_days, :Ny, :Nx]

# # Write to the new NetCDF file
# with Dataset(output_file_path, 'w', format='NETCDF4') as ds:
#     # Define dimensions
#     ds.createDimension('time', all_days)
#     ds.createDimension('lon', Nx)
#     ds.createDimension('lat', Ny)

#     # Create variables
#     times = ds.createVariable('time', 'f4', ('time',))
#     lons = ds.createVariable('lon', 'f4', ('lon',))
#     lats = ds.createVariable('lat', 'f4', ('lat',))
#     pr = ds.createVariable('pr', 'f4', ('time', 'lat', 'lon'), zlib=True)

#     # Add metadata
#     ds.description = 'Non-rotated coordinate precipitation data with TLC integration'
#     ds.source = 'Converted from rotated grid using Python'
#     pr.units = 'mm/day'  # Example, adjust to actual units

#     # Assign values
#     times[:] = np.arange(0, all_days)
#     lons[:] = lon_geo[0, :]  # Assign longitudes for the first row
#     lats[:] = lat_geo[:, 0]  # Assign latitudes for the first column
#     pr[:, :, :] = output_data

# print("Conversion completed. Output saved to:", output_file_path)

"approach 3"
with nc.Dataset(input_file_path) as dataset:
    # Read rotated coordinates and variable
    rlon = dataset.variables['rlon'][:]  # Rotated longitude
    rlat = dataset.variables['rlat'][:]  # Rotated latitude
    pr_data = dataset.variables['pr'][:]  # Precipitation data (time, rlat, rlon)

    # Create 2D rotated coordinate grids
    rlon_2d, rlat_2d = np.meshgrid(rlon, rlat)

    # Convert rotated grid to geographic coordinates using TLC as a reference
    lon_geo, lat_geo = rotated_grid_transform(
        lon_arr=rlon_2d,
        lat_arr=rlat_2d,
        np_lon=rot_pole_lon,
        np_lat=rot_pole_lat,
        direction="rot2geo"
    )

    # Offset geographic coordinates to align with TLC_lat and TLC_lon
    lon_geo += TLC_lon - lon_geo[0, 0]
    lat_geo += TLC_lat - lat_geo[0, 0]

    # Ensure the output grid dimensions match (Ny, Nx)
    lon_geo = lon_geo[:Ny, :Nx]
    lat_geo = lat_geo[:Ny, :Nx]

# Initialize the output data array
output_data = np.zeros((all_days, Ny, Nx), dtype=np.float32)

# Fill the output array (slice the input data to match dimensions)
output_data[:, :, :] = pr_data[:all_days, :Ny, :Nx]

# Write to the new NetCDF file
with Dataset(output_file_path, 'w', format='NETCDF4') as ds:
    # Define dimensions
    ds.createDimension('time', all_days)
    ds.createDimension('lon', Nx)
    ds.createDimension('lat', Ny)

    # Create variables
    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('lon', 'f4', ('lon',))
    lats = ds.createVariable('lat', 'f4', ('lat',))
    pr = ds.createVariable('pr', 'f4', ('time', 'lat', 'lon'), zlib=True)

    # Add metadata
    ds.description = 'Non-rotated coordinate precipitation data with TLC integration'
    ds.source = 'Converted from rotated grid using Python'
    pr.units = 'mm/day'  # Example, adjust to actual units

    # Assign values
    times[:] = np.arange(0, all_days)
    lons[:] = lon_geo[0, :]  # Assign longitudes for the first row
    lats[:] = lat_geo[:, 0]  # Assign latitudes for the first column
    pr[:, :, :] = output_data

print("Conversion completed. Output saved to:", output_file_path)
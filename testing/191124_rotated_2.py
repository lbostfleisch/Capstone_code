"""
File 2: 19.11.24 
Rotating the coordinates 
"""

import xarray as xr
import numpy as np
from pyproj import Proj, transform
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from scipy.interpolate import griddata  


def rotate_coordinates_to_global(lat_r, lon_r, rotated_pole_lat, rotated_pole_lon):
    """
    Rotate the coordinates from a rotated lat/lon grid to a regular global grid.
    lat_r, lon_r: Input rotated latitude and longitude arrays.
    rotated_pole_lat, rotated_pole_lon: Latitude and longitude of the rotation pole.
    """
    # Ensure lat_r and lon_r are 2D grids
    lat_r_grid, lon_r_grid = np.meshgrid(lat_r, lon_r)

    # Compute the difference between the rotated coordinates and the pole coordinates
    lat_global = lat_r_grid + rotated_pole_lat
    lon_global = lon_r_grid + rotated_pole_lon
    
    return lat_global, lon_global

def transform_to_projection(lon, lat, projection_epsg=3034):
    """
    Transform the lat/lon grid to a specific projection, e.g., EPSG:3034 (Lambert Conformal Conic).
    """
    # Set up pyproj transformation
    in_proj = Proj(proj="latlong", datum="WGS84")
    out_proj = Proj(init=f"epsg:{projection_epsg}")

    lon_flat = lon.flatten()
    lat_flat = lat.flatten()

    x, y = transform(in_proj, out_proj, lon_flat, lat_flat)

    return x.reshape(lon.shape), y.reshape(lat.shape)

def regrid_to_new_projection(input_file, output_file, time_index=0):
    # Read the netCDF file using xarray
    ds = xr.open_dataset(input_file)

    # Get the necessary rotation and coordinate information
    lat_r = ds['rlat'].values  # Rotated latitude
    lon_r = ds['rlon'].values  # Rotated longitude
    data = ds['tasmax'].values  # Example variable in the dataset (precipitation)

    print(f"Shape of rotated latitude: {lat_r.shape}")
    print(f"Shape of rotated longitude: {lon_r.shape}")
    print(f"Shape of data variable: {data.shape}")

    # Check that we are selecting the correct time index for data
    if time_index >= data.shape[0]:
        raise ValueError(f"Invalid time index {time_index}. Must be less than {data.shape[0]}.")

    # Select a specific time slice (e.g., time_index=0 for the first time step)
    data_time_slice = data[time_index, :, :]  # Shape: (412, 424)

    # Create a meshgrid of lat_r and lon_r
    lat_r_grid, lon_r_grid = np.meshgrid(lat_r, lon_r)

    # Check that the shapes of the meshgrid match the data dimensions
    if lat_r_grid.shape != data_time_slice.shape:
        raise ValueError(f"Shape mismatch: lat_r_grid {lat_r_grid.shape} and data_time_slice {data_time_slice.shape}")
    if lon_r_grid.shape != data_time_slice.shape:
        raise ValueError(f"Shape mismatch: lon_r_grid {lon_r_grid.shape} and data_time_slice {data_time_slice.shape}")

    # Create a new regular grid (e.g., 180x360 grid)
    new_lat = np.linspace(np.min(lat_r), np.max(lat_r), len(lat_r))
    new_lon = np.linspace(np.min(lon_r), np.max(lon_r), len(lon_r))

    # Create a new grid
    new_lat_grid, new_lon_grid = np.meshgrid(new_lat, new_lon)

    # Interpolate the data variable (e.g., pr) to the new grid
    data_interpolated = griddata(
        (lat_r_grid.flatten(), lon_r_grid.flatten()), 
        data_time_slice.flatten(), 
        (new_lat_grid, new_lon_grid), 
        method='linear'
    )

    # Now apply the rotation to get the global lat/lon
    rotated_pole_lat = ds['lat'].values[0]  # Latitude of the rotated pole
    rotated_pole_lon = ds['lon'].values[0]  # Longitude of the rotated pole

    lat_global, lon_global = rotate_coordinates_to_global(new_lat_grid, new_lon_grid, rotated_pole_lat, rotated_pole_lon)
    
    # Optionally, transform to a specific projection (e.g., EPSG:3034)
    x_proj, y_proj = transform_to_projection(lon_global, lat_global)

    # Create a new dataset with transformed coordinates and the interpolated variable
    new_ds = xr.Dataset(
        {
            'transformed_variable': (['lat', 'lon'], data_interpolated),
        },
        coords={
            'lat': lat_global,
            'lon': lon_global,
        }
    )

    # Save the new dataset to a new NetCDF file
    new_ds.to_netcdf(output_file)



# Example usage:
# input_file = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/original_files/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19660101-19701231.nc'  # Replace with your actual file path
input_file = "D:/Luca_Capstone/a_data_publishing/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/tasmax/orginal_files/tasmax_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19660101-19701231.nc"
output_file = 'C:/03_Capstone/a_publishing/data/test_files_rot/1911_type6_test_rot.nc'


regrid_to_new_projection(input_file, output_file)

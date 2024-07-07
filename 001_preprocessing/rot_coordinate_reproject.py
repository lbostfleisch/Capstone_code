import xarray as xr
from pyproj import CRS, Transformer
import numpy as np

# Open the NetCDF file
file_path = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/tasmax/1970-2005/tasmax_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day_19660101-19701231.nc'
dataset = xr.open_dataset(file_path)

# Extract rotation parameters
rotated_pole = dataset['rotated_pole']
grid_north_pole_latitude = rotated_pole.attrs.get('grid_north_pole_latitude')
print(grid_north_pole_latitude)
grid_north_pole_longitude = rotated_pole.attrs.get('grid_north_pole_longitude')
print(grid_north_pole_longitude)

# Define the rotated CRS using pyproj
rotated_crs = CRS.from_proj4(
    f"+proj=ob_tran +o_proj=longlat +o_lat_p={grid_north_pole_latitude} +o_lon_p={grid_north_pole_longitude} +datum=WGS84 +no_defs"
)

# Define the target European CRS (e.g., ETRS89 / UTM zone 32N)
target_crs = CRS.from_epsg(3034)

# Create a transformer
transformer = Transformer.from_crs(rotated_crs, target_crs)

# Extract rotated coordinates
rotated_lon = dataset['rlon'].values
print(rotated_lon)
rotated_lat = dataset['rlat'].values
print(rotated_lat)
# Create meshgrid of rotated coordinates
rotated_lon_grid, rotated_lat_grid = np.meshgrid(rotated_lon, rotated_lat)

# Flatten the coordinate arrays for transformation
flat_rotated_lon = rotated_lon_grid.flatten()
flat_rotated_lat = rotated_lat_grid.flatten()

# Transform coordinates to the target system
flat_target_lon, flat_target_lat = transformer.transform(flat_rotated_lon, flat_rotated_lat)

# Reshape the transformed coordinates back to the original grid shape
target_lon_grid = flat_target_lon.reshape(rotated_lon_grid.shape)
print("target lon grid", target_lon_grid)
target_lat_grid = flat_target_lat.reshape(rotated_lat_grid.shape)
print("target lat grid:", target_lat_grid)

# Add the transformed coordinates to the dataset
dataset['target_lon'] = (('rlat', 'rlon'), target_lon_grid)
dataset['target_lat'] = (('rlat', 'rlon'), target_lat_grid)

# Save the transformed dataset to a new NetCDF file
output_file_path = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/tasmax/1970-2005/tasmax_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day_19660101-19701231_epsg3034.nc'
dataset.to_netcdf(output_file_path)

print(f"Transformed dataset saved to {output_file_path}")

# Close the dataset
dataset.close()

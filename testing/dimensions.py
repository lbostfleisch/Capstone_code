"""Testing for rotation
printing dimensions
"""
from netCDF4 import Dataset

# Open the NetCDF file (replace 'your_file.nc' with your actual file path)
file_path = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/original_files/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19660101-19701231.nc'  # Replace with your actual file path
nc_file = Dataset(file_path, 'r')

# Extract dimensions
print("Dimensions:")
for dim_name, dim in nc_file.dimensions.items():
    print(f"{dim_name}: size = {len(dim)}")

# Extract variables
print("\nVariables:")
for var_name, var in nc_file.variables.items():
    print(f"{var_name}: dimensions = {var.dimensions}, shape = {var.shape}")

# Close the NetCDF file
nc_file.close()

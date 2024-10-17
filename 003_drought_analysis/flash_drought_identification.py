"""
file for flash drought identification
17.10.24
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# File path setup (modify to match your environment)
directory = "C:/03_Capstone/Data/Future/ssp585/02_run2_160324/"
file_name = "one_grid_cell_2_ssp585_spei_2015-2100_obsgevpara.nc"

# Open the NetCDF file and extract data
with Dataset(f"{directory}{file_name}", mode="r") as nc:
    array = nc.variables['spei'][:]  # Extract the SPEI data
    fill_value = nc.variables['spei']._FillValue  # Handle missing values

# Replace fill values with NaN
array = np.where(array == fill_value, np.nan, array)

# Initialize variables
period = 4
# period = 4
len_loop = len(array) - period + 1
dif = np.full(len_loop, np.nan)  # Create an array of NaNs

# Sliding window calculation
# for t in range(len_loop):
#     window = array[t:t + period]

#     if np.isnan(window).sum() <= 2:  # Process only if there are fewer than 3 NaNs
#         max_idx, min_idx = np.nanargmax(window), np.nanargmin(window)
#         dif[t] = np.nanmax(window) - np.nanmin(window) if min_idx < max_idx else np.nanmin(window) - np.nanmax(window)


# period = 4
flash_drought = np.zeros(len_loop, dtype=bool)  # Store flash drought detections

for t in range(len_loop):
    window = array[t:t + period]

    if np.isnan(window).sum() > 0:  # Skip windows with NaN values
        continue

    # Condition 1: Check if the drop is 2 or more
    drop = window[0] - window[-1]  # Compare first and last values in the window
    if drop >= 2:
        # Condition 2: Check if final SPEI is less than -1.28
        if window[-1] < -1.28:
            flash_drought[t] = True  # Mark as flash drought

# Add padding to align with the original data length
# test2 = np.concatenate(([0, 0, 0], dif, [0, 0, 0]))

# # Create a DataFrame for plotting
# df = pd.DataFrame({
#     'x': np.arange(1, len(array) + 1),
#     'line': array,
#     'bar': test2,
#     'flash_drought': (test2 < -2) & (array < -1.28)
# })

df = pd.DataFrame({
    'x': np.arange(1, len(array) + 1),
    'line': array,
    'flash_drought': np.concatenate([flash_drought, [False] * (len(array) - len(flash_drought))])
})

# Plotting the results
# def plot_flash_drought(df, title):
#     plt.figure(figsize=(10, 5))
#     plt.plot(df['x'], df['line'], color='gray', linewidth=1.2, label='SPEI')
#     plt.scatter(df[df['flash_drought']]['x'], df[df['flash_drought']]['bar'], color='red', label='Flash Drought')
#     plt.vlines(df[df['flash_drought']]['x'], ymin=0, ymax=df[df['flash_drought']]['bar'], color='red')
#     plt.axhline(y=0, color='black', linewidth=1)
#     plt.axhline(y=-1.28, color='black', linestyle='dashed')
#     plt.ylim(-3, 3)
#     plt.legend()
#     plt.title(title)
#     plt.show()

# # Generate plots
# plot_flash_drought(df, "Flash Drought Detection - Plot 1")

plt.figure(figsize=(10, 5))
plt.plot(df['x'], df['line'], color='gray', linewidth=1.2, label='SPEI')
plt.scatter(df[df['flash_drought']]['x'], df[df['flash_drought']]['line'], color='red', label='Flash Drought')
plt.axhline(y=0, color='black', linewidth=1)
plt.axhline(y=-1.28, color='black', linestyle='dashed')
plt.ylim(-4, 4)
plt.legend()
plt.title("Flash Drought Detection")
plt.show()

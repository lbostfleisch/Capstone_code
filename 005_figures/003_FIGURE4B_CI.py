""" 
13.05.24
Figure to depict the 99% confidence interval 
"""
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mpl
from scipy.stats import linregress
from scipy.stats import genextreme



mpl.rcParams['font.family'] = 'Times New Roman'

input_file_ssp126 = "C:/03_Capstone/Data/Future/ssp126/run1_200324/ssp126_spei_2015-2100_obsgevpara.nc"
input_ssp126 = Dataset(input_file_ssp126, 'r')

input_file_ssp585 = "C:/03_Capstone/Data/Future/ssp585/02_run2_160324/ssp585_spei_2015-2100_obsgevpara.nc"
input_ssp585 = Dataset(input_file_ssp585, 'r')

var = 'spei'
lon = input_ssp126['lon'][:]
lat = input_ssp126['lat'][:]
time = input_ssp126['time'][:]

"plotting the confidence interval "
# confidence_intervals = []

# for year in range(2015, 2100+1, 1):
#     a = year - 2015
#     color_index = a
    
#     if a == 0: 
#         start_day = 0 
#         end_day = 364 
#     elif ((a + 1) % 4) == 0:  # +1 because 2016 is a leap year 
#         end_day += 366
#         start_day = end_day - 365
#     else: 
#         end_day += 365 
#         start_day = end_day - 364
        
#     data = input_ssp126.variables[var][start_day:end_day, :, :].flatten()
#     data_without_nan = data[~np.isnan(data)]
#     mu, sigma = norm.fit(data_without_nan)  # Fit data to a normal distribution

#     # Calculate 99% confidence interval
#     lower_bound, upper_bound = norm.interval(0.99, loc=mu, scale=sigma)
#     confidence_intervals.append((lower_bound, upper_bound))

# # Plotting the confidence intervals
# years = range(2015, 2100+1)
# plt.fill_between(years, [ci[0] for ci in confidence_intervals], [ci[1] for ci in confidence_intervals], color='gray', alpha=0.3)
# plt.xlabel('Year')
# plt.ylabel('Value')
# plt.title('99% Confidence Interval over Time')
# plt.show()

"top one percent"

# top_1_percent_values = []
# top_1_percent_values_ssp585 = []

# years = range(2015, 2100+1)

# for year in years:
#     a = year - 2015
    
#     if a == 0: 
#         start_day = 0 
#         end_day = 364 
#     elif ((a + 1) % 4) == 0:  # +1 because 2016 is a leap year 
#         end_day += 366
#         start_day = end_day - 365
#     else: 
#         end_day += 365 
#         start_day = end_day - 364
        
#     data_ssp126 = input_ssp126.variables[var][start_day:end_day, :, :].flatten()
#     data_without_nan_ssp126 = data_ssp126[~np.isnan(data_ssp126)]
#     top_1_percent_ssp126 = np.percentile(data_without_nan_ssp126, 1)
#     top_1_percent_values.append(top_1_percent_ssp126)

#     data_ssp585 = input_ssp585.variables[var][start_day:end_day, :, :].flatten()
#     data_without_nan_ssp585 = data_ssp585[~np.isnan(data_ssp585)]
#     top_1_percent_ssp585 = np.percentile(data_without_nan_ssp585, 1)
#     top_1_percent_values_ssp585.append(top_1_percent_ssp585)

# # Fit linear regression model
# slope_ssp126, intercept_ssp126, _, _, _ = linregress(years, top_1_percent_values)
# slope_ssp585, intercept_ssp585, _, _, _ = linregress(years, top_1_percent_values_ssp585)


# # Plotting the top 1% values with trendline
# plt.plot(years, top_1_percent_values, marker='o', linestyle='', color='orange', markersize=3)
# plt.plot(years, top_1_percent_values_ssp585, marker='o', linestyle='', color='red', markersize=3)
# plt.plot(years, [slope_ssp126 * year + intercept_ssp126 for year in years], color='orange', label='SSP126 Trendline')
# plt.plot(years, [slope_ssp585 * year + intercept_ssp585 for year in years], color='red', label='SSP585 Trendline')

# plt.xlabel('Year')
# plt.ylabel('SPEI Value')
# plt.title('Top 1% Values over Time with Trendline')
# plt.legend()
# plt.show()

"plotting the variance"
num_rows = 2
num_colm = 1

fig, axes = plt.subplots(num_rows, num_colm, figsize=(15, 10))


variance_values = []
variance_values_585 = []

years = range(2015, 2100+1)

for year in range(2015, 2100+1, 1):
    a = year - 2015
    
    if a == 0: 
        start_day = 0 
        end_day = 364 
    elif ((a + 1) % 4) == 0:  # +1 because 2016 is a leap year 
        end_day += 366
        start_day = end_day - 365
    else: 
        end_day += 365 
        start_day = end_day - 364
        
    data = input_ssp126.variables[var][start_day:end_day, :, :].flatten()
    data_without_nan = data[~np.isnan(data)]
    variance = np.var(data_without_nan)
    variance_values.append(variance)

    data_585 = input_ssp585.variables[var][start_day:end_day, :, :].flatten()
    data_without_nan_585 = data_585[~np.isnan(data_585)]
    variance_585 = np.var(data_without_nan_585)
    variance_values_585.append(variance_585)


slope_ssp126, intercept_ssp126, _, _, _ = linregress(years, variance_values)
slope_ssp585, intercept_ssp585, _, _, _ = linregress(years, variance_values_585)


# Plotting the variance over time
axes[0].plot(range(2015, 2100+1), variance_values, marker='', linestyle='-', color='orange')
axes[0].plot(range(2015, 2100+1), variance_values_585, marker='', linestyle='-', color='red')

axes[0].plot(years, [slope_ssp126 * year + intercept_ssp126 for year in years], color='orange', label='SSP126 Trendline')
axes[0].plot(years, [slope_ssp585 * year + intercept_ssp585 for year in years], color='red', label='SSP585 Trendline')

axes[0].set_xlabel('Year')
axes[0].set_ylabel('Variance')
axes[0].set_title('Variance of Data over Time')
# axes[0].plt.grid(True)
axes[0].legend()
# plt.show()


"plotting the shape parameter of the gev distribution"
shape_values_ssp126 = []
shape_values_ssp585 = []

years = range(2015, 2100+1)

for year in years:
    a = year - 2015
    
    if a == 0: 
        start_day = 0 
        end_day = 364 
    elif ((a + 1) % 4) == 0:  # +1 because 2016 is a leap year 
        end_day += 366
        start_day = end_day - 365
    else: 
        end_day += 365 
        start_day = end_day - 364
    
    data = input_ssp126.variables[var][start_day:end_day, :, :].flatten()
    data_without_nan = data[~np.isnan(data)]
    filtered_data = data_without_nan[np.isfinite(data_without_nan)]
    shape_gev, loc_gev, scale_gev = genextreme.fit(filtered_data)

    data_ssp585 = input_ssp585.variables[var][start_day:end_day, :, :].flatten()
    data_without_nan_ssp585 = data_ssp585[~np.isnan(data_ssp585)]
    filtered_data_ssp585 = data_without_nan_ssp585[np.isfinite(data_without_nan_ssp585)]
    shape_gev_585, loc_gev_585, scale_gev_585 = genextreme.fit(filtered_data_ssp585)

    shape_values_ssp126.append(shape_gev)
    shape_values_ssp585.append(shape_gev_585)
    print("year:", year)

slope_ssp126, intercept_ssp126, _, _, _ = linregress(years, shape_values_ssp126)
slope_ssp585, intercept_ssp585, _, _, _ = linregress(years, shape_values_ssp585)

axes[1].plot(range(2015, 2100+1), shape_values_ssp126, marker='', linestyle='-', color='orange')
axes[1].plot(range(2015, 2100+1), shape_values_ssp585, marker='', linestyle='-', color='red')
axes[1].plot(years, [slope_ssp126 * year + intercept_ssp126 for year in years], color='orange', label='SSP126 Trendline')
axes[1].plot(years, [slope_ssp585 * year + intercept_ssp585 for year in years], color='red', label='SSP585 Trendline')

    
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Shape of GEV distribution')
axes[1].set_title('Shape of GEV distribution of SPEI values over Time')
axes[1].legend()

plt.tight_layout()
plt.show()
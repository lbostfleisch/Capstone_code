"""
03.05.24

trying first to model based imputation for the values 
"""
import numpy as np
import xarray as xr
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.init as init
from sklearn.metrics import r2_score
import torch.nn.functional as F
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split




"loading and handling the nan in the high res data"
# high_res_historical_ds = xr.open_dataset('C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT/obs_spei_1970-2014.nc')
# X_high_res = high_res_historical_ds['spei'].values  # High-resolution historical data

# # Identify missing values indices
# missing_indices_high = np.isnan(X_high_res)
# non_missing_indices_high = ~missing_indices_high

# # Select features and target for training
# X_train_high = X_high_res[non_missing_indices_high].reshape(-1, 1)  # Reshape if necessary
# y_train_high = X_high_res[non_missing_indices_high]

# # Preprocess the data to handle missing values
# imputer_high = SimpleImputer(strategy='mean')
# X_train_imputed_high = imputer_high.fit_transform(X_train_high)

# # Initialize and train the model
# model_high = LinearRegression()
# model_high.fit(X_train_imputed_high, y_train_high)

# # Predict missing values using the trained model
# X_missing_high = X_high_res[missing_indices_high].reshape(-1, 1)  # Reshape if necessary
# X_missing_imputed_high = imputer_high.transform(X_missing_high)
# imputed_values_high = model_high.predict(X_missing_imputed_high)

# # Replace missing values in X_high_res with imputed values
# X_high_res[missing_indices_high] = imputed_values_high

# # Convert the NumPy array back to an xarray DataArray
# data_array_high = xr.DataArray(X_high_res, dims=('time', 'lon', 'lat'),
#                           coords={'time': high_res_historical_ds['time'],
#                                   'lon': high_res_historical_ds['lon'],
#                                   'lat': high_res_historical_ds['lat']})

# # Create a new xarray Dataset with the imputed data
# imputed_dataset_high = xr.Dataset({'spei': data_array_high})

# # Save the imputed dataset to a NetCDF file
# imputed_dataset_high.to_netcdf('C:/03_Capstone/Data/Downscale/his-his/highres_nanfill.nc')
# print("imputed and saved the high res dataset ")

""
"loading and handling the nan in the low res data"
# low_res_historical_ds = xr.open_dataset("C:/03_Capstone/Data/Future/historical/run2_140324/his_spei_1970-2014_obsgevpara.nc")
# X_low_res = low_res_historical_ds['spei'].values 

# # Identify missing values indices
# missing_indices_low = np.isnan(X_low_res)
# non_missing_indices_low = ~missing_indices_low

# # Select features and target for training
# X_train_low = X_low_res[non_missing_indices_low].reshape(-1, 1)  # Reshape if necessary
# y_train_low = X_low_res[non_missing_indices_low]

# # Preprocess the data to handle missing values
# imputer_low = SimpleImputer(strategy='mean')
# X_train_imputed_low = imputer_low.fit_transform(X_train_low)

# # Initialize and train the model
# model_low = LinearRegression()
# model_low.fit(X_train_imputed_low, y_train_low)

# # Predict missing values using the trained model
# X_missing_low = X_low_res[missing_indices_low].reshape(-1, 1)  # Reshape if necessary
# X_missing_imputed_low = imputer_low.transform(X_missing_low)
# imputed_values_low = model_low.predict(X_missing_imputed_low)

# # Replace missing values in X_high_res with imputed values
# X_low_res[missing_indices_low] = imputed_values_low

# # Convert the NumPy array back to an xarray DataArray
# data_array_low = xr.DataArray(X_low_res, dims=('time', 'lon', 'lat'),
#                           coords={'time': low_res_historical_ds['time'],
#                                   'lon': low_res_historical_ds['lon'],
#                                   'lat': low_res_historical_ds['lat']})

# # Create a new xarray Dataset with the imputed data
# imputed_dataset_low = xr.Dataset({'spei': data_array_low})

# # Save the imputed dataset to a NetCDF file
# imputed_dataset_low.to_netcdf('C:/03_Capstone/Data/Downscale/his-his/lowres_nanfill.nc')
# print("imputed and saved the low res dataset")


###########
"loading and handling the FUTURE data"
# # fut_res_historical_ds = xr.open_dataset("C:/03_Capstone/Data/Future/ssp126/run1_200324/ssp126_spei_2015-2100_obsgevpara.nc")
# fut_res_historical_ds = xr.open_dataset("C:/03_Capstone/Data/Future/ssp585/02_run2_160324/ssp585_spei_2015-2100_obsgevpara.nc")
# X_fut_res = fut_res_historical_ds['spei'].values 

# # Identify missing values indices
# missing_indices_fut = np.isnan(X_fut_res)
# non_missing_indices_fut = ~missing_indices_fut

# # Select features and target for training
# X_train_fut = X_fut_res[non_missing_indices_fut].reshape(-1, 1)  # Reshape if necessary
# y_train_fut = X_fut_res[non_missing_indices_fut]

# # Preprocess the data to handle missing values
# imputer_fut = SimpleImputer(strategy='mean')
# X_train_imputed_fut = imputer_fut.fit_transform(X_train_fut)

# # Initialize and train the model
# model_fut = LinearRegression()
# model_fut.fit(X_train_imputed_fut, y_train_fut)

# # Predict missing values using the trained model
# X_missing_fut = X_fut_res[missing_indices_fut].reshape(-1, 1)  # Reshape if necessary
# X_missing_imputed_fut = imputer_fut.transform(X_missing_fut)
# imputed_values_fut = model_fut.predict(X_missing_imputed_fut)

# # Replace missing values in X_high_res with imputed values
# X_fut_res[missing_indices_fut] = imputed_values_fut

# # Convert the NumPy array back to an xarray DataArray
# data_array_fut = xr.DataArray(X_fut_res, dims=('time', 'lon', 'lat'),
#                           coords={'time': fut_res_historical_ds['time'],
#                                   'lon': fut_res_historical_ds['lon'],
#                                   'lat': fut_res_historical_ds['lat']})

# # Create a new xarray Dataset with the imputed data
# imputed_dataset_fut = xr.Dataset({'spei': data_array_fut})

# # Save the imputed dataset to a NetCDF file
# imputed_dataset_fut.to_netcdf('C:/03_Capstone/Data/Downscale/ssp585/ssp585_futres_nanfill.nc')
# print("imputed and saved the fut res dataset")


##############################################################################
"beginning with the downscaling"
high_res_path_clean = xr.open_dataset("C:/03_Capstone/Data/Downscale/his-his/highres_nanfill.nc")
high_res_var_clean = high_res_path_clean['spei'].values

low_res_path_clean = xr.open_dataset('C:/03_Capstone/Data/Downscale/his-his/lowres_nanfill.nc')
low_res_var_clean = low_res_path_clean['spei'].values

y_train_high, y_test_high = train_test_split(high_res_var_clean, test_size=0.2, random_state=42)
X_train_low, X_test_low = train_test_split(low_res_var_clean, test_size=0.2, random_state=42)

# Converting to PyTorch tensors
y_train_tensor = torch.tensor(y_train_high, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test_high, dtype=torch.float32)
print("y_train_tensor_high shape:", y_train_tensor.shape, "\n", "y_test_tensor_high shape:", y_test_tensor.shape)

X_train_tensor = torch.tensor(X_train_low, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test_low, dtype=torch.float32)
print("X_train_tensor_low shape:", X_train_tensor.shape, "\n", "X_test_tensor_low shape:", X_test_tensor.shape)

"more complex version"

class DownscalingModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, dropout_prob):
        super(DownscalingModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size) #all based on linearity 
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.dropout = nn.Dropout(dropout_prob)
        self.init_weights()

    def init_weights(self):   #weights important for convergence 
        init.xavier_uniform_(self.fc1.weight)
        init.xavier_uniform_(self.fc2.weight)
        init.xavier_uniform_(self.fc3.weight)
        init.constant_(self.fc1.bias, 0)
        init.constant_(self.fc2.bias, 0)
        init.constant_(self.fc3.bias, 0)

    def forward(self, x):   #forward pass of the model. defines how data is handled when passing through model 
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x

# Update input_size, output_size, and add hidden_size
input_size = 7 * 10
hidden_size = 300  #number of units in the hidden layers
#orig: 256
output_size = 59 * 77
dropout_prob = 0.5  #dropout probability, which determines the probability of dropping out units during training (to avoid overfitting)
#orig: 0.5

"model"
model = DownscalingModel(input_size, hidden_size, output_size, dropout_prob)


# X_train_flattened = X_train_tensor.view(X_train_tensor.size(0), -1)
# print("X_train_flattened shape:", X_train_flattened.shape)
# y_train_flattened = y_train_tensor.view(y_train_tensor.size(0), -1)
# print("y_train_flattened shape:", y_train_flattened.shape)
# print("model", model)

criterion = nn.MSELoss()  
optimizer = optim.Adam(model.parameters(), lr=0.001)  #lr = learning rate 
num_epochs = 200
batch_size = 128   #adjust if necessary

# losses = [] 

# for epoch in range(num_epochs):
#     model.train()
#     running_loss = 0.0
    
#     for i in range(0, len(X_train_flattened), batch_size):
#         optimizer.zero_grad()
#         # print("X_train_flattened:", X_train_flattened)
#         batch_input = X_train_flattened[i:i+batch_size]
#         # print("Batch input:", batch_input)
#         # # skipping the cells with an input of 0 
#         # mask1 = (~torch.isnan(batch_input))
#         # batch_input = batch_input[mask1]
#         # print(batch_input)
#         # print(model)
#         outputs = model(batch_input)
#         # print("output:", outputs)
#         # mask2 = (~torch.isnan(batch_target))
#         # batch_target = y_train_flattened[i:i+batch_size][mask2]
#         batch_target = y_train_flattened[i:i+batch_size]
#         # print("Batch target", batch_target)
#         loss = criterion(outputs, batch_target)
#         # print("loss", loss)
#         loss.backward()
#         optimizer.step()
#         running_loss += loss.item() * batch_input.size(0)

#     epoch_loss = running_loss / len(X_train_flattened)
#     losses.append(epoch_loss)

#     # Print epoch statistics
#     print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}')

# # Save the trained model

# torch.save(model.state_dict(), 'C:/03_Capstone/Data/Downscale/ssp126/downscale_050524_lr001_bs128_hs300_dp5_epoch200.pth')
# print("saved the model")

# plt.plot(range(1, num_epochs + 1), losses)
# plt.xlabel('Epochs')
# plt.ylabel('Training Loss')
# plt.title('Training Loss over Epochs')
# plt.grid(True)
# plt.show()





########################################################
"loading in the dataset to be downscaled"

saved_model_path = 'C:/03_Capstone/Data/Downscale/ssp126/downscale_050524_lr001_bs128_hs300_dp5_epoch200.pth'
model = DownscalingModel(input_size, hidden_size, output_size, dropout_prob)
model.load_state_dict(torch.load(saved_model_path))

dataset = xr.open_dataset('C:/03_Capstone/Data/Downscale/his-his/lowres_nanfill.nc')
# dataset = xr.open_dataset('C:/03_Capstone/Data/Future/ssp126/run1_200324/ssp126_spei_2015-2100_obsgevpara.nc')
data_tensor = torch.tensor(dataset['spei'].values, dtype=torch.float32)
data_flattened = data_tensor.view(data_tensor.size(0), -1)

with torch.no_grad():
    predictions = model(data_flattened)
    print("predictions", predictions)
    print("predictions shape:", predictions.shape)

# r2 = r2_score(y_train_flattened, predictions)
# print(f'R-squared: {r2:.4f}')

reshaped_predictions = predictions.reshape(16435, 59, 77)   #for size of past 
# reshaped_predictions = predictions.reshape(31411, 59, 77)   #for size of future 


print("reshaped_predictions shape:", reshaped_predictions.shape)

predicted_data_array = xr.DataArray(reshaped_predictions.numpy(), dims=('time', 'lon', 'lat'),
                                     coords={'time': dataset['time'],
                                             'lon': high_res_path_clean['lon'],
                                             'lat': high_res_path_clean['lat']})

predicted_dataset = xr.Dataset({'predicted_spei': predicted_data_array})
predicted_dataset.to_netcdf('C:/03_Capstone/Data/Downscale/his-his/downscale_hismodel_110524_lr001_bs128_hs300_dp5_epoch200.nc')


########################################################
"evaluating the model with the testing data"
model.eval()

X_test_tensor = torch.tensor(X_test_low, dtype=torch.float32)
data_flattened_eval = X_test_tensor.view(X_test_tensor.size(0), -1)


with torch.no_grad():
    # Forward pass to get predictions
    predictions_eval = model(data_flattened_eval)

predictions_eval = predictions_eval.numpy()
reshaped_predictions_eval = predictions_eval.reshape(3287, 59, 77)   #3287 is the time size of the testing data 

mse = np.mean((reshaped_predictions_eval - y_test_high) ** 2)    #mean squared error  #need to check if it is really y_test_high and not the tensor thereof 
print("Mean square error:", mse)
rmse = np.sqrt(mse)    #root mean square error 
print("root mean square error:", rmse)

# print("y_test_high shape", y_test_high.shape)
# print("reshaped_predictions_eval shape:", reshaped_predictions_eval.shape)
y_test_high_flattened = y_test_high.flatten()
# print("y_test_high_flattened shape:", y_test_high_flattened.shape)
reshaped_predictions_eval_flat = reshaped_predictions_eval.flatten()
# print("reshaped_predictions_eval_flat shape", reshaped_predictions_eval_flat.shape)
r2 = r2_score(y_test_high_flattened, reshaped_predictions_eval_flat)
print("R-squared:", r2)
######################################################

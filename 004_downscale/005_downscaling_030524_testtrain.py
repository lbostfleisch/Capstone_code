"""
purpose: downscale the low resolution future data based on the patterns between the high resolution observational and low resolution past data 
    the file contains the following steps: 
    1A) loading and handling any nan values of the high resolution past modeled data set through imputing
    1B) loading and handling any nan values of the low resolution observational data set through imputing
    1C) loading and handling any nan values of the high resolution future modeled data set through imputing
    2) training the model 
    3) downscaling the future data 
    4) evaluate the model 

author: Luca Boestfleisch, but following: Ng, R. (2024, February 26). ritchieng/deep-learning-wizard: LLM Section Release. Zenodo. https://zenodo.org/badge/latestdoi/139945544
last updated: 03.05.24
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




"STEP 1A: loading and handling the nan in the high resolution data"
high_res_historical_ds = xr.open_dataset('') #adapt 
X_high_res = high_res_historical_ds['spei'].values #adapt the variable name 

# Identify missing values indices
missing_indices_high = np.isnan(X_high_res)
non_missing_indices_high = ~missing_indices_high

# Select features and target for training
X_train_high = X_high_res[non_missing_indices_high].reshape(-1, 1)  
y_train_high = X_high_res[non_missing_indices_high]

# Preprocess the data to handle missing values
imputer_high = SimpleImputer(strategy='mean')
X_train_imputed_high = imputer_high.fit_transform(X_train_high)

# Initialize and train the model
model_high = LinearRegression()
model_high.fit(X_train_imputed_high, y_train_high)

# Predict missing values using the trained model
X_missing_high = X_high_res[missing_indices_high].reshape(-1, 1)  
X_missing_imputed_high = imputer_high.transform(X_missing_high)
imputed_values_high = model_high.predict(X_missing_imputed_high)

# Replace missing values in X_high_res with imputed values
X_high_res[missing_indices_high] = imputed_values_high

# Convert the NumPy array back to an xarray DataArray
data_array_high = xr.DataArray(X_high_res, dims=('time', 'lon', 'lat'),
                          coords={'time': high_res_historical_ds['time'],
                                  'lon': high_res_historical_ds['lon'],
                                  'lat': high_res_historical_ds['lat']})

# Create a new xarray Dataset with the imputed data
imputed_dataset_high = xr.Dataset({'spei': data_array_high})

# Save the imputed dataset to a NetCDF file
imputed_dataset_high.to_netcdf('') #adapt 
print("imputed and saved the high res dataset")


"Step 1B: loading and handling the nan in the low resolution data"
low_res_historical_ds = xr.open_dataset("") #adapt 
X_low_res = low_res_historical_ds['spei'].values #adapt the variable name 

# Identify missing values indices
missing_indices_low = np.isnan(X_low_res)
non_missing_indices_low = ~missing_indices_low

# Select features and target for training
X_train_low = X_low_res[non_missing_indices_low].reshape(-1, 1)  
y_train_low = X_low_res[non_missing_indices_low]

# Preprocess the data to handle missing values
imputer_low = SimpleImputer(strategy='mean')
X_train_imputed_low = imputer_low.fit_transform(X_train_low)

# Initialize and train the model
model_low = LinearRegression()
model_low.fit(X_train_imputed_low, y_train_low)

# Predict missing values using the trained model
X_missing_low = X_low_res[missing_indices_low].reshape(-1, 1)  
X_missing_imputed_low = imputer_low.transform(X_missing_low)
imputed_values_low = model_low.predict(X_missing_imputed_low)

# Replace missing values in X_high_res with imputed values
X_low_res[missing_indices_low] = imputed_values_low

# Convert the NumPy array back to an xarray DataArray
data_array_low = xr.DataArray(X_low_res, dims=('time', 'lon', 'lat'),
                          coords={'time': low_res_historical_ds['time'],
                                  'lon': low_res_historical_ds['lon'],
                                  'lat': low_res_historical_ds['lat']})

# Create a new xarray Dataset with the imputed data
imputed_dataset_low = xr.Dataset({'spei': data_array_low})

# Save the imputed dataset to a NetCDF file
imputed_dataset_low.to_netcdf('') #adapt 
print("imputed and saved the low res dataset")


###########
"STEP 1C: loading and handling the FUTURE data"
fut_res_historical_ds = xr.open_dataset("") #adapt 
X_fut_res = fut_res_historical_ds['spei'].values #adapt the variable name 

# Identify missing values indices
missing_indices_fut = np.isnan(X_fut_res)
non_missing_indices_fut = ~missing_indices_fut

# Select features and target for training
X_train_fut = X_fut_res[non_missing_indices_fut].reshape(-1, 1)  
y_train_fut = X_fut_res[non_missing_indices_fut]

# Preprocess the data to handle missing values
imputer_fut = SimpleImputer(strategy='mean')
X_train_imputed_fut = imputer_fut.fit_transform(X_train_fut)

# Initialize and train the model
model_fut = LinearRegression()
model_fut.fit(X_train_imputed_fut, y_train_fut)

# Predict missing values using the trained model
X_missing_fut = X_fut_res[missing_indices_fut].reshape(-1, 1)  
X_missing_imputed_fut = imputer_fut.transform(X_missing_fut)
imputed_values_fut = model_fut.predict(X_missing_imputed_fut)

# Replace missing values in X_high_res with imputed values
X_fut_res[missing_indices_fut] = imputed_values_fut

# Convert the NumPy array back to an xarray DataArray
data_array_fut = xr.DataArray(X_fut_res, dims=('time', 'lon', 'lat'),
                          coords={'time': fut_res_historical_ds['time'],
                                  'lon': fut_res_historical_ds['lon'],
                                  'lat': fut_res_historical_ds['lat']})

# Create a new xarray Dataset with the imputed data
imputed_dataset_fut = xr.Dataset({'spei': data_array_fut})

# Save the imputed dataset to a NetCDF file
imputed_dataset_fut.to_netcdf('') #adapt 
print("imputed and saved the fut res dataset")


##############################################################################
"STEP 2: training the model"
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

'define the below parameters as necessary'
input_size = 7 * 10
hidden_size = 300  #number of units in the hidden layers
output_size = 59 * 77
dropout_prob = 0.5  #dropout probability, which determines the probability of dropping out units during training (to avoid overfitting)

model = DownscalingModel(input_size, hidden_size, output_size, dropout_prob)

"flattening the variables"
X_train_flattened = X_train_tensor.view(X_train_tensor.size(0), -1)
print("X_train_flattened shape:", X_train_flattened.shape)
y_train_flattened = y_train_tensor.view(y_train_tensor.size(0), -1)
print("y_train_flattened shape:", y_train_flattened.shape)
print("model", model)

criterion = nn.MSELoss()  
optimizer = optim.Adam(model.parameters(), lr=0.001)  #lr = learning rate 
num_epochs = 200
batch_size = 128   #adjust if necessary

losses = [] 

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    
    for i in range(0, len(X_train_flattened), batch_size):
        optimizer.zero_grad()
        # print("X_train_flattened:", X_train_flattened)
        batch_input = X_train_flattened[i:i+batch_size]
        # print("Batch input:", batch_input)
        # # skipping the cells with an input of 0 
        # mask1 = (~torch.isnan(batch_input))
        # batch_input = batch_input[mask1]
        # print(batch_input)
        # print(model)
        outputs = model(batch_input)
        # print("output:", outputs)
        # mask2 = (~torch.isnan(batch_target))
        # batch_target = y_train_flattened[i:i+batch_size][mask2]
        batch_target = y_train_flattened[i:i+batch_size]
        # print("Batch target", batch_target)
        loss = criterion(outputs, batch_target)
        # print("loss", loss)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * batch_input.size(0)

    epoch_loss = running_loss / len(X_train_flattened)
    losses.append(epoch_loss)

    # Print epoch statistics
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}')


torch.save(model.state_dict(), '') #adapt the path to which the model should save 
print("saved the model")

plt.plot(range(1, num_epochs + 1), losses)
plt.xlabel('Epochs')
plt.ylabel('Training Loss')
plt.title('Training Loss over Epochs')
plt.grid(True)
plt.show()





########################################################
"STEP 3: loading in the dataset to be downscaled"

saved_model_path = '' #adapt 
model = DownscalingModel(input_size, hidden_size, output_size, dropout_prob)
model.load_state_dict(torch.load(saved_model_path))

dataset = xr.open_dataset('') #adapt 
data_tensor = torch.tensor(dataset['spei'].values, dtype=torch.float32)
data_flattened = data_tensor.view(data_tensor.size(0), -1)

with torch.no_grad():
    predictions = model(data_flattened)
    print("predictions", predictions)
    print("predictions shape:", predictions.shape)



reshaped_predictions = predictions.reshape(16435, 59, 77)  #define the file dimensions 

print("reshaped_predictions shape:", reshaped_predictions.shape)

predicted_data_array = xr.DataArray(reshaped_predictions.numpy(), dims=('time', 'lon', 'lat'),
                                     coords={'time': dataset['time'],
                                             'lon': high_res_path_clean['lon'],
                                             'lat': high_res_path_clean['lat']})

predicted_dataset = xr.Dataset({'predicted_spei': predicted_data_array})
predicted_dataset.to_netcdf('') #adapt 


########################################################
"STEP 4: evaluating the model with the testing data"
model.eval()

X_test_tensor = torch.tensor(X_test_low, dtype=torch.float32)
data_flattened_eval = X_test_tensor.view(X_test_tensor.size(0), -1)


with torch.no_grad():
    predictions_eval = model(data_flattened_eval)

predictions_eval = predictions_eval.numpy()
reshaped_predictions_eval = predictions_eval.reshape(3287, 59, 77)   #adapt to the dimensions of the dataset  

"mean squared error"
mse = np.mean((reshaped_predictions_eval - y_test_high) ** 2)   
print("Mean square error:", mse)

'root mean squared error'
rmse = np.sqrt(mse)    
print("root mean square error:", rmse)

'r2'
y_test_high_flattened = y_test_high.flatten()
reshaped_predictions_eval_flat = reshaped_predictions_eval.flatten()
r2 = r2_score(y_test_high_flattened, reshaped_predictions_eval_flat)
print("R-squared:", r2)
######################################################

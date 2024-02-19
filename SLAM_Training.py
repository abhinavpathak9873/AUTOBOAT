import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.impute import SimpleImputer
import joblib


# Step 1: Load Data
data = pd.read_csv('SLAM_training_data/slam_training_data.csv')

# Step 2: Prepare Features and Targets
X = data.drop(columns=['x', 'y','direction'])
y = data[['x', 'y','direction']]

# Step 3: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Handle missing values with -1
#imputer = SimpleImputer(strategy='constant', fill_value=-1)
#X_train_filled = imputer.fit_transform(X_train)

# Step 5: Drop columns with all -1 values
X_train_filtered = X_train.loc[:, (X_train != -1).any(axis=0)]
X_test_filtered = X_test.loc[:, (X_test != -1).any(axis=0)]

# Step 6: Implement Random Forest
model = RandomForestRegressor()

# Step 7: Train the Model
model.fit(X_train, y_train)

# Step 8: Evaluate the Model
#X_test_filled = imputer.transform(X_test)  # Impute missing values in the test set
y_pred = model.predict(X_test)
print(X_test, y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("Mean Absolute Error:", mae)
print("Mean Squared Error:", mse)


# Save the model
joblib.dump(model, 'pos_estimation.pkl')
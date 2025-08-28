#
# Client Efficiency Prediction using TensorFlow
#
# This script builds and trains a neural network to predict client efficiency
# based on daily operational data for rented construction machinery.
#
import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import io

# --- 1. Data Loading and Preparation ---
# Load the data from the provided CSV file.
try:
    df = pd.read_csv('client_daily_data.csv')
except FileNotFoundError:
    print("Error: 'client_daily_data.csv' not found.")
    print("Please make sure the CSV file is in the same directory as the script.")
    # As a fallback for demonstration, create a dummy dataframe
    df = pd.DataFrame({
        'Date': ['2023-01-01'], 'MachineType': ['Excavator'], 'ActiveOperatingHours': [0],
        'IdleTime': [0], 'FuelConsumption(L)': [0], 'AvgLoad(Tonnes)': [0],
        'MaxLoad(Tonnes)': [0], 'AvgEngineRPM': [0], 'AvgHydraulicPressure(PSI)': [0],
        'WeatherConditions': ['Clear'], 'SiteConditions': ['Dry'], 'SupportingStaff': [0],
        'ClientEfficiency': [0.5]
    })


# Drop the 'Date' column as it's not a direct feature for this daily prediction model
df = df.drop('Date', axis=1)

# --- 2. Feature Engineering and Preprocessing ---

# Separate features (X) from the target variable (y)
X = df.drop('ClientEfficiency', axis=1)
y = df['ClientEfficiency']

# Identify categorical and numerical features
categorical_features = ['MachineType', 'WeatherConditions', 'SiteConditions']
numerical_features = X.select_dtypes(include=np.number).columns.tolist()

# Create a preprocessing pipeline
# - OneHotEncoder: Converts categorical text data into a numerical format.
# - StandardScaler: Scales numerical features to have a mean of 0 and variance of 1.
#   This helps the neural network learn more effectively.
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply the preprocessing pipeline to the data
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

# --- 3. Build the Neural Network Model ---

# We use a Sequential model, which is a linear stack of layers.
model = tf.keras.models.Sequential([
    # Input layer: The shape must match the number of features after preprocessing.
    tf.keras.layers.Input(shape=(X_train_processed.shape[1],)),

    # Hidden Layer 1: 64 neurons with a ReLU activation function.
    # ReLU is a common choice for hidden layers.
    tf.keras.layers.Dense(64, activation='relu'),

    # Hidden Layer 2: 32 neurons, also with ReLU activation.
    tf.keras.layers.Dense(32, activation='relu'),

    # Output Layer: 1 neuron because we are predicting a single value (efficiency).
    # The 'sigmoid' activation function squashes the output to a range between 0 and 1,
    # which is perfect for our efficiency score.
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# --- 4. Compile the Model ---

# 'adam' is an efficient and popular optimization algorithm.
# 'mean_squared_error' is a standard loss function for regression problems
# where we are predicting a continuous value.
model.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=['mean_absolute_error']) # Track MAE for easier interpretation

# Print a summary of the model's architecture
print("Model Summary:")
model.summary()

# --- 5. Train the Model ---

print("\n--- Training the model ---")
# 'epochs' is the number of times the model will cycle through the entire training dataset.
# 'validation_split' reserves a portion of the training data to evaluate the
# model's performance at the end of each epoch.
history = model.fit(
    X_train_processed,
    y_train,
    epochs=100,
    validation_split=0.2,
    verbose=1 # Set to 0 to hide epoch-by-epoch training logs
)

# --- 6. Evaluate the Model ---

print("\n--- Evaluating the model on the test set ---")
loss, mae = model.evaluate(X_test_processed, y_test, verbose=0)

print(f"Test Set Mean Squared Error: {loss:.4f}")
print(f"Test Set Mean Absolute Error: {mae:.4f}")
print(f"\nThis means the model's predictions are, on average, off by about {mae:.2f} from the actual efficiency score.")


# --- 7. Make Predictions on New Data ---

print("\n--- Making a prediction on a sample new data point ---")

# Create a sample data point that mimics the original DataFrame structure
new_data = pd.DataFrame([{
    'MachineType': 'Excavator',
    'ActiveOperatingHours': 8.0,
    'IdleTime': 1.5,
    'FuelConsumption(L)': 410,
    'AvgLoad(Tonnes)': 15.5,
    'MaxLoad(Tonnes)': 20.0,
    'AvgEngineRPM': 1900,
    'AvgHydraulicPressure(PSI)': 3600,
    'WeatherConditions': 'Clear',
    'SiteConditions': 'Dry',
    'SupportingStaff': 5
}])

# Use the same preprocessor to transform the new data
new_data_processed = preprocessor.transform(new_data)

# Predict the efficiency
predicted_efficiency = model.predict(new_data_processed)[0][0]

print(f"\nPredicted efficiency for the new data: {predicted_efficiency:.2f}")
joblib.dump(preprocessor, "saved_model/preprocessor_client.pkl")

model.save("saved_model/client_efficiency_model.keras")
# Save the trained model for future use
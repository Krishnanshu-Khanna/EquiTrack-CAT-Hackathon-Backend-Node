# -*- coding: utf-8 -*-
"""
This script trains a TensorFlow neural network to predict the actual time
a construction project will take based on various operational, contextual,
and client-related features.

The process includes:
1. Loading the dataset from a CSV file.
2. Cleaning and preprocessing the data (handling non-numeric values,
   scaling numerical features, and one-hot encoding categorical features).
3. Building a sequential neural network model with dense layers.
4. Compiling and training the model.
5. Evaluating the model's performance on a test set.
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
# --- 1. Load and Prepare the Data ---

# Load the dataset from the CSV file
try:
    df = pd.read_csv('construction_machine_rental_Data.csv')
except FileNotFoundError:
    print("Error: The CSV file was not found.")
    print("Please make sure 'construction_machine_rental_Data (2).csv' is in the same directory.")
    exit()


# --- 2. Preprocessing ---

# Clean up column names for easier access
# Removes spaces, special characters, and converts to lowercase
df.columns = df.columns.str.replace(r'[^A-Za-z0-9]+', '_', regex=True).str.lower()

# The 'contractvalue' column contains commas and needs to be converted to a number.
# We remove the commas and cast the column to a float type.
if 'contractvalue' in df.columns:
    df['contractvalue'] = df['contractvalue'].replace({',': ''}, regex=True).astype(float)

# Define the features (X) and the target (y)
# The target variable is 'actualtime_months', which we want to predict.
X = df.drop('actualtime_months', axis=1)
y = df['actualtime_months']

# Identify categorical and numerical features for preprocessing
categorical_features = ['typeofproject', 'weather_season', 'machinetype', 'sitedemographic']
numerical_features = [col for col in X.columns if col not in categorical_features]

# Create a preprocessing pipeline to handle both feature types
# Numerical features will be scaled to have a mean of 0 and a standard deviation of 1.
# Categorical features will be converted into a numerical format using one-hot encoding.
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply the preprocessing steps to the training and testing data
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

# --- 3. Build the TensorFlow Model ---

# Define the neural network architecture
# This is a sequential model with three hidden layers.
model = tf.keras.Sequential([
    # Input layer: The shape must match the number of processed features
    tf.keras.layers.Dense(128, activation='relu', input_shape=[X_train_processed.shape[1]]),
    
    # Hidden layers with dropout to prevent overfitting
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.2), # Dropout randomly sets 20% of input units to 0
    
    tf.keras.layers.Dense(32, activation='relu'),
    
    # Output layer: A single neuron to predict the continuous 'ActualTime' value
    tf.keras.layers.Dense(1)
])

# --- 4. Compile the Model ---

# Configure the model for training
# Optimizer: Adam is an efficient and commonly used optimization algorithm.
# Loss Function: Mean Absolute Error (MAE) is a good choice for regression,
# as it measures the average magnitude of the errors in a set of predictions.
model.compile(optimizer='adam',
              loss='mae',
              metrics=['mae', 'mse']) # Mean Squared Error is also monitored

# Print a summary of the model's architecture
model.summary()

# --- 5. Train the Model ---

print("\n--- Starting Model Training ---")
# Train the model on the processed training data for 100 epochs
# An epoch is one complete pass through the entire training dataset.
# Validation data is used to monitor the model's performance on unseen data during training.
history = model.fit(
    X_train_processed,
    y_train,
    epochs=100,
    validation_data=(X_test_processed, y_test),
    verbose=1 # Set to 0 to hide epoch-by-epoch logging
)
print("--- Model Training Finished ---\n")


# --- 6. Evaluate the Model ---

print("--- Evaluating Model Performance on Test Data ---")
loss, mae, mse = model.evaluate(X_test_processed, y_test, verbose=2)

print(f"\nTest Set Mean Absolute Error (MAE): {mae:.2f} months")
print(f"This means, on average, the model's prediction is off by about {mae:.2f} months.")
print(f"Test Set Mean Squared Error (MSE): {mse:.2f}")


# --- 7. Make and Display Predictions ---

# Use the trained model to make predictions on the test set
predictions = model.predict(X_test_processed).flatten()

# Create a DataFrame to compare actual values with predictions
results_df = pd.DataFrame({
    'Actual Time (months)': y_test,
    'Predicted Time (months)': predictions
})

# Round the predictions for cleaner display
results_df['Predicted Time (months)'] = results_df['Predicted Time (months)'].round(2)

print("\n--- Sample Predictions vs. Actual Values ---")
# Display the first 10 predictions for a quick comparison
print(results_df.head(10))
joblib.dump(preprocessor, "saved_model/preprocessor_time.pkl")
model.save("saved_model/time_prediction_model.keras")

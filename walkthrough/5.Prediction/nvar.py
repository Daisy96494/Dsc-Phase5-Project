import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

def generate_time_series(df, target_col, lag=10):
    """
    Constructs time-delay embeddings and polynomial features.
    df: DataFrame containing weather data.
    target_col: The column to predict.
    lag: Number of past time steps to use as features.
    """
    X, Y = [], []
    for i in range(len(df) - lag - 1):
        X.append(df[target_col].iloc[i:i+lag].values)
        Y.append(df[target_col].iloc[i+lag+1])
    
    X = np.array(X)
    Y = np.array(Y)
    
    # Add nonlinear polynomial features (up to cubic)
    X_poly = np.hstack([X, X**2, X**3])
    return X_poly, Y

def train_nvar(X, Y, alpha=1e-3):
    """Trains a Ridge regression model."""
    model = Ridge(alpha=alpha)
    model.fit(X, Y)
    return model

def predict_nvar(model, X_init, steps=100):
    """
    Iteratively predicts future values using trained NVAR model.
    """
    predictions = []
    current_input = X_init.copy()
    
    for _ in range(steps):
        pred = model.predict(current_input.reshape(1, -1))[0]
        predictions.append(pred)
        
        # Shift input for next prediction
        current_input = np.roll(current_input, -1)
        current_input[-1] = pred
    
    return np.array(predictions)

def evaluate_predictions(y_true, y_pred):
    """Computes normalized RMSE."""
    return np.sqrt(mean_squared_error(y_true, y_pred)) / (np.max(y_true) - np.min(y_true))

def plot_predictions(y_true, y_pred, title="Weather Forecast with NVAR"):
    """Plots actual vs. predicted values."""
    plt.figure(figsize=(10, 5))
    plt.plot(y_true, label='Actual', linestyle='dashed')
    plt.plot(y_pred, label='Predicted')
    plt.legend()
    plt.title(title)
    plt.show()

# Example usage with dummy weather data
df = pd.DataFrame({"temperature": np.sin(np.linspace(0, 10, 200)) + np.random.normal(0, 0.1, 200)})

# Train & Predict
X, Y = generate_time_series(df, target_col="temperature", lag=10)
model = train_nvar(X, Y)
predictions = predict_nvar(model, X[-1], steps=50)

y_true = df["temperature"].iloc[-50:].values
error = evaluate_predictions(y_true, predictions)
print(f"NRMSE: {error:.4f}")

plot_predictions(y_true, predictions)

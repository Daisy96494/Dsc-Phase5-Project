import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler

# Generate synthetic time series data
def generate_synthetic_data(n=500):
    np.random.seed(42)
    time = np.arange(n)
    values = np.sin(time / 10) + np.random.normal(scale=0.3, size=n)
    
    # Introduce anomalies
    anomalies = np.random.choice(n, size=int(0.05 * n), replace=False)
    values[anomalies] += np.random.normal(scale=2, size=len(anomalies))
    
    return pd.DataFrame({'time': time, 'value': values})

# Train Isolation Forest model for anomaly detection
def train_isolation_forest(data, contamination=0.05):
    scaler = MinMaxScaler()
    normalized_values = scaler.fit_transform(data[['value']])
    
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(normalized_values)
    
    # Predict anomaly scores
    scores = model.decision_function(normalized_values)
    anomalies = model.predict(normalized_values)
    
    # Convert scores to probability using MinMax scaling
    probability_scores = (scores - scores.min()) / (scores.max() - scores.min())
    
    data['anomaly_score'] = scores
    data['probability'] = probability_scores
    data['is_anomaly'] = anomalies == -1
    
    return data, model

# Plot time series with anomalies
def plot_anomalies(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data['time'], data['value'], label='Time Series Data', color='blue')
    
    anomalies = data[data['is_anomaly']]
    plt.scatter(anomalies['time'], anomalies['value'], color='red', label='Anomalies', marker='x')
    
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Anomaly Detection in Time Series Data')
    plt.legend()
    plt.show()

# Main execution
data = generate_synthetic_data()
data, model = train_isolation_forest(data)
plot_anomalies(data)

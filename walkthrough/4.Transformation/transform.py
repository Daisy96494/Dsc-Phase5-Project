from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
import time
import json
import pandas as pd
import numpy as np
from kafka import KafkaProducer

app = FastAPI()



# Kafka Configuration
KAFKA_BROKER = "kafka:9092"  # Make sure it matches docker-compose

KAFKA_TOPIC = "transformed_weather_data"

# Directory to monitor
AGGREGATE_DIR = "/app/downloads/aggregate"

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# Track last processed file
last_processed_file = None

def get_latest_aggregate_file():
    """Get the most recent CSV file in the aggregate directory."""
    files = [f for f in os.listdir(AGGREGATE_DIR) if f.endswith(".csv")]
    if not files:
        return None
    return max(files, key=lambda f: os.path.getmtime(os.path.join(AGGREGATE_DIR, f)))

def parse_temperature(entry):
    try:
        temp_str, _ = entry.split(",")
        return int(temp_str) / 10 if temp_str != "99999" else None
    except:
        return None

def parse_rainfall(entry):
    try:
        parts = entry.split(",")
        return None if int(parts[1]) == 99999 else int(parts[1]) / 10
    except:
        return None

def parse_ceiling_height(entry):
    try:
        parts = entry.split(",")
        return None if parts[0] == "99999" else int(parts[0])
    except:
        return None

def parse_visibility(entry):
    try:
        parts = entry.split(",")
        return None if parts[0] == "99999" else int(parts[0]) / 10
    except:
        return None

def parse_sl_pressure(entry):
    try:
        parts = entry.split(",")
        return None if parts[0] == "99999" else int(parts[0]) / 10
    except:
        return None

def parse_dew(entry):
    try:
        parts = entry.split(",")
        return None if int(parts[0]) == 99999 else int(parts[0])
    except:
        return None

def parse_wind_speed(entry):
    try:
        parts = entry.split(",")
        return None if parts[3] == "99999" else int(parts[3]) / 10
    except:
        return None

def parse_wind_dir(entry):
    try:
        parts = entry.split(",")
        return None if parts[0] == "99999" else int(parts[0])
    except:
        return None

def impute_missing_values(df):
    for col in df.columns:
        missing_mask = df[col].isna()
        if missing_mask.any():
            median = df[col].median()
            mean_median_product = df[col].mean() * median
            lower_bound = mean_median_product if df[col].lt(0).any() else 0
            np.random.seed(int(median) if not np.isnan(median) else None)
            df.loc[missing_mask, col] = np.random.uniform(lower_bound, mean_median_product, missing_mask.sum())
    return df

def process_data(file_path):
    data = pd.read_csv(file_path)
    
    data['WND'] = data['WND'].apply(parse_wind_speed)
    data['AA1'] = data['AA1'].apply(parse_rainfall)
    data['TMP'] = data['TMP'].apply(parse_temperature)
    data['SLP'] = data['SLP'].apply(parse_sl_pressure)
    data['DEW'] = data['DEW'].apply(parse_dew)
    
    rescols = ['WND', 'AA1', 'TMP', 'SLP', 'DEW']
    filtered_data = data[rescols]
    filtered_data = impute_missing_values(filtered_data)
    return filtered_data.to_dict(orient='records')


@app.get("/health")
def home():
    return {"message": "Transform service running"}


@app.post("/transform")
def transform_and_push():
    """Process the latest aggregate file and push transformed data to Kafka."""
    global last_processed_file
    
    latest_file = get_latest_aggregate_file()
    
    if not latest_file or latest_file == last_processed_file:
        return
    
    file_path = os.path.join(AGGREGATE_DIR, latest_file)
    print(f"Processing new aggregate file: {latest_file}")

    cleaned_data = process_data(file_path)
    for record in cleaned_data:
        producer.send(KAFKA_TOPIC, record)
    producer.flush()
    print("Data transformation complete. Pushed to Kafka.")

    last_processed_file = latest_file

if __name__ == "__main__":
    print("Starting Transform Service...")
    while True:
        transform_and_push()
        time.sleep(10)  # Poll every 10 seconds

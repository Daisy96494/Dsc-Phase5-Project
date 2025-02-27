from fastapi import FastAPI, HTTPException
import requests
import sys
import os
import pandas as pd
from bs4 import BeautifulSoup
import random
from .db import stationYears_collection

app = FastAPI()


@app.get("/health")
def home():
    return {"message": "Ingestion service running"}


# Base URLs
LOOKUP_API_URL = "http://lookup_service:8001/lookup"
BASE_NOAA_URL = "https://www.ncei.noaa.gov/data/global-hourly/access/"

# Get available years for a given station
def get_station_years(station_id):
    record = stationYears_collection.find_one({"station_id": station_id})
    return record["years"] if record else []

def get_stations_with_year_ranges(city, limit=3):
    valid_stations = []
    has_recent_data = False  # Flag for 2024/2025 presence

    while limit < 8:
        response = requests.get(f"{LOOKUP_API_URL}?city={city}&limit={limit}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch station IDs")

        station_ids = response.json().get("nearest_stations", [])
        formatted_stations = [f"{station['usaf']}{station['wban']}.csv" for station in station_ids]

        for station_id in formatted_stations:
            record = stationYears_collection.find_one({"station_id": station_id})
            
            if not record:  # If station isn't in MongoDB, trigger lookup
                lookup_resp = requests.get(f"{LOOKUP_API_URL}?city={city}&limit={limit}")
                if lookup_resp.status_code == 200:
                    station_ids = lookup_resp.json().get("nearest_stations", [])
                    formatted_stations = [f"{station['usaf']}{station['wban']}.csv" for station in station_ids]

                record = stationYears_collection.find_one({"station_id": station_id})  # Retry fetching

            if record:
                years = sorted(map(int, record["years"]), reverse=True)
                if years:
                    start_year = years[0]
                    valid_years = [years[0]]

                    for i in range(1, len(years)):
                        if years[i - 1] - years[i] == 1:
                            valid_years.append(years[i])
                        else:
                            break  # Stop if there's a gap

                    if 2024 in valid_years or 2025 in valid_years:
                        has_recent_data = True
                    
                    valid_stations.append({"station_id": station_id, "years_range": f"{valid_years[0]}-{valid_years[-1]}"})

        if has_recent_data:
            break

        limit += random.randint(1, 3)

    return valid_stations


# Fetch station data with year ranges
@app.get("/fetch_stations")
def fetch_stations(city: str):
    stations = get_stations_with_year_ranges(city)
    if not stations:
        raise HTTPException(status_code=404, detail="No stations found in database")
    return {"stations": stations}

# Download and recursively merge data
def download_and_merge_station_data(station_id, years):
    downloads_dir = "downloads"
    aggregate_dir = os.path.join(downloads_dir, "aggregate")
    
    # Ensure directories exist
    os.makedirs(downloads_dir, exist_ok=True)
    os.makedirs(aggregate_dir, exist_ok=True)

    merged_file = os.path.join(aggregate_dir, f"{station_id}_combined.csv")
    temp_files = []  # List to track downloaded CSVs

    for year in years:
        file_name = station_id
        url = f"{BASE_NOAA_URL}{year}/{file_name}"
        output_path = os.path.join(downloads_dir, f"{file_name}_{year}.csv")

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(output_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            temp_files.append(output_path)  # Track downloaded file
            
            # Merge process
            if os.path.exists(merged_file):
                df_existing = pd.read_csv(merged_file, low_memory=False)
                df_new = pd.read_csv(output_path, low_memory=False)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined.to_csv(merged_file, index=False)
            else:
                df_new = pd.read_csv(output_path, low_memory=False)
                df_new.to_csv(merged_file, index=False)
        
        except requests.exceptions.RequestException:
            continue  # Skip failed downloads

    # ✅ Remove all individual station-year CSVs after merging
    for file in temp_files:
        os.remove(file)

    return merged_file if os.path.exists(merged_file) else None

# Ingest data recursively
@app.get("/ingest_data")
def ingest_data(station_id: str):
    try:
        available_years = sorted(map(int, get_station_years(station_id)), reverse=True)
        if not available_years:
            raise HTTPException(status_code=404, detail="No valid years available for ingestion")
        
        merged_file = download_and_merge_station_data(station_id, available_years)
        return {"message": "Process completed", "merged_file": merged_file if merged_file else "No data downloaded"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

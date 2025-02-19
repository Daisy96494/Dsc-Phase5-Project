import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import random
import json  # To store the collection of years as JSON

# Base URL for NOAA data
base_url = "https://www.ncei.noaa.gov/data/global-hourly/access/"

# Function to fetch the page with retries
def fetch_with_retry(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()  # Check for HTTP errors
            return response
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(delay + random.uniform(1, 3))  # Exponential backoff with randomness
            else:
                raise
    return None  # If all retries fail, return None

# Function to get stations for a given year
def get_stations_for_year(year):
    year_url = f"{base_url}{year}/"
    response = fetch_with_retry(year_url)
    if response is None:
        print(f"Failed to fetch stations for year {year}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all links for .csv files
    stations = []
    for a_tag in soup.find_all("a", href=True):
        station_file = a_tag["href"]
        if station_file.endswith(".csv"):  # Ensure it's a CSV file
            stations.append(station_file.strip("/"))
    
    return stations

# Function to get all years
def get_years():
    response = fetch_with_retry(base_url)
    if response is None:
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")

    years = []
    for a_tag in soup.find_all("a", href=True):
        year = a_tag['href'].strip('/')
        if year.isdigit():
            years.append(year)
    
    return sorted(years)

# Function to store stations and their years in the SQLite database
def store_stations_in_db(stations_by_year):
    # Connect to SQLite database
    conn = sqlite3.connect('stations_by_year.db')
    cursor = conn.cursor()

    # Create table (if not exists) with station_id as the key and years as a collection (JSON)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS station_data (
        station_id TEXT PRIMARY KEY,
        years TEXT
    )
    ''')

    # Insert data into the table
    for station, years in stations_by_year.items():
        # Convert the years list to a JSON string
        years_json = json.dumps(years)
        
        cursor.execute('''
            INSERT OR REPLACE INTO station_data (station_id, years)
            VALUES (?, ?)
        ''', (station, years_json))
    
    conn.commit()
    conn.close()
    print("Station data stored in database.")

# Function to fetch and organize stations by year
def scrape_and_store_stations():
    years = get_years()
    stations_by_year = {}

    for year in years:
        print(f"Fetching stations for year {year}...")
        stations = get_stations_for_year(year)
        
        # Organize stations by year
        for station in stations:
            if station not in stations_by_year:
                stations_by_year[station] = []
            stations_by_year[station].append(year)
    
    # Store the organized data in the database
    store_stations_in_db(stations_by_year)

# Run the scraping and storage process
scrape_and_store_stations()

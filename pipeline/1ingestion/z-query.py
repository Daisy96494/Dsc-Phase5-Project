import sqlite3
import requests
import os
import json
import pandas as pd

# Base URL for NOAA data
base_url = "https://www.ncei.noaa.gov/data/global-hourly/access/"

# Function to get available years for a given station ID
def get_station_years(station_id):
    conn = sqlite3.connect('stations_by_year.db')
    cursor = conn.cursor()
    cursor.execute('SELECT years FROM station_data WHERE station_id = ?', (station_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return json.loads(result[0])  # Convert stored JSON back to a list
    else:
        return None

# Function to download a file
def download_file(url, output_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Function to download and merge CSV files
def download_and_merge_station_data(station_id, start_year, end_year):
    os.makedirs("downloads", exist_ok=True)  # Ensure directory exists
    file_paths = []
    
    for year in range(start_year, end_year + 1):
        url = f"{base_url}{year}/{station_id}"
        output_path = os.path.join("downloads", f"{station_id}_{year}.csv")
        
        # Download the file
        download_file(url, output_path)
        file_paths.append(output_path)
    
    # Merge all CSV files
    print("\nMerging downloaded files into one...")
    combined_file = os.path.join("downloads", f"{station_id}_combined.csv")
    
    try:
        df_list = [pd.read_csv(file, low_memory=False) for file in file_paths]
        combined_df = pd.concat(df_list, ignore_index=True)
        combined_df.to_csv(combined_file, index=False)
        print(f"\nMerged file saved as: {combined_file}")
    except Exception as e:
        print(f"Error merging files: {e}")

# Main execution flow
def main():
    station_id = input("Enter station ID (e.g., 01001099999.csv): ").strip()
    
    years = get_station_years(station_id)
    if not years:
        print("No data found for this station.")
        return
    
    print(f"\nAvailable years for {station_id}: {', '.join(years)}")
    
    # Get start and end year input from the user
    try:
        start_year = int(input("Enter start year from the available list: ").strip())
        end_year = int(input("Enter end year from the available list: ").strip())

        if str(start_year) not in years or str(end_year) not in years or start_year > end_year:
            print("Invalid input. Ensure both years are within the available range and valid.")
            return

        # Proceed with downloading and merging
        download_and_merge_station_data(station_id, start_year, end_year)
    
    except ValueError:
        print("Invalid input. Please enter a valid year.")

if __name__ == "__main__":
    main()

import os
import pandas as pd
import argparse

# Function declarations
def parse_temp(entry):
    if isinstance(entry, str) and entry != "99999":
        temp_str, _ = entry.split(",")
        return int(temp_str) / 10
    return None

def parse_rainfall(entry):
    if isinstance(entry, str) and entry != "99999":
        parts = entry.split(",")
        if len(parts) != 4:
            return None
        try:
            return float(parts[0]) / 10  # Ensuring it is a float
        except ValueError:
            return None
    return None

def parse_vis(entry):
    if isinstance(entry, str) and entry != "99999":
        parts = entry.split(",")
        if len(parts) != 4 or entry == "999999,9,9,9":  # Invalid visibility data
            return None
        return None if parts[0] == "99999" else float(parts[0]) / 10  # Ensuring visibility is a float
    return None

def parse_slp(entry):
    if isinstance(entry, str) and entry != "99999":
        parts = entry.split(",")
        if len(parts) != 2:
            return None
        return None if parts[0] == "99999" else int(parts[0]) / 10
    return None

def parse_dew(entry):
    if isinstance(entry, str) and entry != "99999":
        parts = entry.split(",")
        if len(parts) != 2:
            return None
        return int(parts[0])
    return None

def parse_wind_speed(entry):
    if isinstance(entry, str) and entry != "99999":
        parts = entry.split(",")
        if len(parts) != 5 or entry == "999,9,9,9999,9":  # Invalid wind data
            return None
        return None if parts[3] == "99999" else int(parts[3]) / 10
    return None

def parse_elevation(entry):
    if entry == "99999":
        return None
    try:
        return float(entry)
    except (ValueError, TypeError):
        return None

def clean_weather_data(filepath):
    # Residual Columns
    rescols = ['NAME', 'ELEVATION', 'DATE', 'WND', 'AA1', 'TMP', 'SLP', 'DEW']
    
    # Load data
    df = pd.read_csv(filepath)
    existing_cols = [col for col in rescols if col in df.columns]
    data = df[existing_cols]
    
    # Parsing block
    if 'ELEVATION' in data.columns:
        data['ELEVATION'] = data['ELEVATION'].apply(parse_elevation)
    if 'WND' in data.columns:
        data['WND'] = data['WND'].apply(parse_wind_speed)
    if 'AA1' in data.columns:
        data['AA1'] = data['AA1'].apply(parse_rainfall)
    if 'TMP' in data.columns:
        data['TMP'] = data['TMP'].apply(parse_temp)
    if 'SLP' in data.columns:
        data['SLP'] = data['SLP'].apply(parse_slp)
    if 'DEW' in data.columns:
        data['DEW'] = data['DEW'].apply(parse_dew)
    if 'VIS' in data.columns:
        data['VIS'] = data['VIS'].apply(parse_vis)
    
    # Create output filename
    dirname, filename = os.path.split(filepath)
    name, ext = os.path.splitext(filename)
    cleaned_filename = f"{name}_cleaned{ext}"
    cleaned_filepath = os.path.join(dirname, "cleaneddata", cleaned_filename)
    
    # Ensure output directory exists
    os.makedirs(os.path.join(dirname, "cleaneddata"), exist_ok=True)
    
    # Save cleaned data
    data.to_csv(cleaned_filepath, index=False)
    print(f"Cleaned data saved to: {cleaned_filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean weather data CSV file.")
    parser.add_argument("filepath", type=str, help="Path to the CSV file")
    args = parser.parse_args()
    clean_weather_data(args.filepath)

import sqlite3
import pandas as pd

# File paths
csv_file = "./isd-history.csv"
database = "../../climatrack/db.sqlite3"
table_name = "station_data"

# Connect to SQLite database
conn = sqlite3.connect(database)
cursor = conn.cursor()

# Read and execute schema.sql
with open("./init.sql", "r") as file:
    schema = file.read()
cursor.executescript(schema)
conn.commit()

# Load only the required columns from CSV
columns_to_keep = ["USAF", "WBAN", "STATION NAME", "LAT", "LON"]
df = pd.read_csv(csv_file, usecols=columns_to_keep, dtype=str)  # Read only needed columns

# Rename columns to match database schema
df.rename(columns={
    "USAF": "usaf",
    "WBAN": "wban",
    "STATION NAME": "station_name",
    "LAT": "latitude",
    "LON": "longitude"
}, inplace=True)

# Convert latitude and longitude to numeric (invalid values become NaN)
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

# Drop rows where any of the required columns have NULL values
df.dropna(subset=["usaf", "wban", "station_name", "latitude", "longitude"], inplace=True)

# Insert into SQLite
df.to_sql(table_name, conn, if_exists="replace", index=False)

# Verify data insertion
cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
print(cursor.fetchall())

# Close connection
conn.close()

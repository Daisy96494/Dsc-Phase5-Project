import sqlite3
import pandas as pd

# File paths
csvfile = './worldcities.csv'
database = '../../climatrack/db.sqlite3'
table_name = 'location_data'

# Connect to SQLite
conn = sqlite3.connect(database)

# Load CSV into pandas DataFrame
df = pd.read_csv(csvfile)

# Keep only the necessary columns
required_columns = {
    "city": "city",
    "country": "country",
    "iso3": "iso3",
    "lat": "latitude",   # Rename lat → latitude
    "lng": "longitude"   # Rename lng → longitude
}

# Drop unwanted columns and rename required ones
df = df[list(required_columns.keys())].rename(columns=required_columns)

# Insert into SQLite (append new data)
df.to_sql(table_name, conn, if_exists="append", index=False, method="multi")

# Close connection
conn.close()

print("Data successfully loaded into the database!")

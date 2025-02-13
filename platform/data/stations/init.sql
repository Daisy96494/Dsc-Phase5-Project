CREATE TABLE IF NOT EXISTS station_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usaf TEXT,
    wban TEXT,
    station_name TEXT,
    latitude REAL,
    longitude REAL
);

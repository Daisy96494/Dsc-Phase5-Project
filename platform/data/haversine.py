import sqlite3
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in km

# Connect to the database
conn = sqlite3.connect("../climatrack/db.sqlite3")
cursor = conn.cursor()

# Get the location's coordinates
location_name = "Mumbai"
cursor.execute("SELECT latitude, longitude FROM location_data WHERE city = ?", (location_name,))
location = cursor.fetchone()

if location:
    lat1, lon1 = location
    cursor.execute("SELECT usaf, station_name, latitude, longitude FROM station_data")
    stations = cursor.fetchall()

    # Find the closest station
    closest_station = min(stations, key=lambda s: haversine(lat1, lon1, s[2], s[3]))

    print(f"Closest station: {closest_station[1]} (ID: {closest_station[0]}) at {closest_station[2]}, {closest_station[3]}")
else:
    print("Location not found")

# Close connection
conn.close()

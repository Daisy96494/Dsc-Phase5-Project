import sqlite3
import json


def get_station_years(station_id):
    conn = sqlite3.connect('stations_by_year.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT years FROM station_data WHERE station_id = ?
    ''', (station_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        # Convert the JSON string back into a list of years
        return json.loads(result[0])
    else:
        return None


test = get_station_years('94374099999.csv')

print(test)
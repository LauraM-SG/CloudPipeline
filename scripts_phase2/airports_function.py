import functions_framework 
import pandas as pd
import requests
import dotenv
import os
import pymysql
from sqlalchemy import create_engine

dotenv.load_dotenv()

@functions_framework.http
def airports(request):

    API_key = os.getenv('OpenWeatherAPIKey')
    RapidAPIKey=os.getenv('RapidAPIKey')
    username = os.getenv('username')
    mysql_password = os.getenv('mysql_password')
    
    schema = "gans"
    host = "34.77.218.163"
    port = 3306
   
    connection_string = f"mysql+pymysql://{username}:{mysql_password}@{host}:{port}/{schema}"
    engine = create_engine(connection_string)

    query = "SELECT * FROM cities"
    cities_df = pd.read_sql(query, con=engine)
    all_airports = []  

    for _, row in cities_df.iterrows():  # Iterate through rows to get both city_name & city_id
        city = row["city_name"]
        city_id = row["city_id"]

        # Get city coordinates from OpenWeather API
        geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_key}'
        geo_json = requests.get(geo_url).json()

        if not geo_json:
            print(f"No coordinates found for {city}.")
            continue  # Skip to the next city

        lat, lon = geo_json[0]['lat'], geo_json[0]['lon']

        # AeroDataBox API configuration
        headers = {
            "X-RapidAPI-Key": RapidAPIKey,
            "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
        }

        querystring = {"withFlightInfoOnly": "true"}
        url = f"https://aerodatabox.p.rapidapi.com/airports/search/location/{lat}/{lon}/km/50/16"

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code != 200:
            print(f"Error fetching airports for {city}: {response.status_code}")
            continue  # Skip to the next city

        data = response.json()

        if "items" not in data or not data["items"]:
            print(f"No airports found near {city}.")
            continue  # Skip to the next city

        # Extract only needed fields
        existing_icaos = pd.read_sql("SELECT icao FROM airports", con=engine)["icao"].tolist()

        for airport in data["items"]:
            icao_code = airport.get("icao", None)
            if icao_code in existing_icaos:  # Si ya existe, saltarlo
                continue
        
            airport_data = {
                "city_id": city_id,
                "airport_name": airport.get("name", None), 
                "icao": airport.get("icao", None),
                "iata": airport.get("iata", None),
                "latitude": airport.get("location", {}).get("lat", None),
                "longitude": airport.get("location", {}).get("lon", None),
            }
            all_airports.append(airport_data)

    if all_airports:
        new_airports_df = pd.DataFrame(all_airports)
        new_airports_df.to_sql(name="airports", con=engine, if_exists="append", index=False)
        return "Data successfully added"
    else:
        return "No new airports to add"
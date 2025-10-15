import functions_framework # type: ignore
import pandas as pd
import requests
import dotenv
import os
import pymysql
from sqlalchemy import create_engine
from pytz import timezone
from datetime import datetime

dotenv.load_dotenv()

@functions_framework.http
def city_forecast(request):
    tz = 'Europe/Berlin'
    API_key = os.getenv('OpenWeatherAPIKey')
    username = os.getenv('username')
    mysql_password = os.getenv('mysql_password')
  
    schema = "gans"
    host = "34.77.218.163"
    port = 3306
   
    connection_string = f"mysql+pymysql://{username}:{mysql_password}@{host}:{port}/{schema}"
    engine = create_engine(connection_string)

    query = "SELECT * FROM cities"
    cities_df = pd.read_sql(query, con=engine)

    all_forecasts = []     
    
    for _, row in cities_df.iterrows():  
        city = row["city_name"]
        city_id = row["city_id"] 
       
        geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_key}'
        geo_json = requests.get(geo_url).json()

        if not geo_json:
            print(f"Error getting coords for {city}.")
            continue

        lat, lon = geo_json[0]['lat'], geo_json[0]['lon']
 
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=metric"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Error getting forecast metrics for {city}: {response.status_code}")
            continue

        weather_json = response.json()
        time_retrieved = datetime.now(timezone(tz))
 
        for forecast in weather_json["list"][:40]: 
            main_data = {
                "city_id": city_id, 
                "forecast_date": forecast["dt_txt"], 
                "weather_desc": forecast.get("weather", [{}])[0].get("main", None),
                "temp": forecast.get("main", {}).get("temp", None),
                "feels_like": forecast.get("main", {}).get("feels_like", None),
                "temp_min": forecast.get("main", {}).get("temp_min", None),
                "temp_max": forecast.get("main", {}).get("temp_max", None),
                "humidity": forecast.get("main", {}).get("humidity", None),
                "wind_speed": forecast.get("wind", {}).get("speed", None),
                "visibility": forecast.get("visibility", None), 
                "pop": forecast.get("pop", None),
                "rain": forecast.get("rain", {}).get("3h", None),
                "snow": forecast.get("snow", {}).get("3h", None),
                "time_retrieved": time_retrieved
            }
            all_forecasts.append(main_data)
    
    city_forecast_df = pd.DataFrame(all_forecasts)
    city_forecast_df["forecast_date"] = pd.to_datetime(city_forecast_df["forecast_date"])
    city_forecast_df["time_retrieved"] = pd.to_datetime(city_forecast_df["time_retrieved"])

    city_forecast_df.to_sql(name="weather",con=connection_string, if_exists="append",index=False)

    return "Data succesfully added"
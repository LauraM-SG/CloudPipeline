
import functions_framework 
import pandas as pd
import requests
import dotenv
import os
import pymysql
import time
from sqlalchemy import create_engine
from pytz import timezone
from datetime import datetime, timedelta

dotenv.load_dotenv()

@functions_framework.http
def arrival_flight_info(request):

    API_key = os.getenv('RapidAPIKey')
    username = os.getenv('username')
    mysql_password = os.getenv('mysql_password')
    
    schema = "gans"
    host = "34.77.218.163"
    port = 3306
   
    connection_string = f"mysql+pymysql://{username}:{mysql_password}@{host}:{port}/{schema}"
    engine = create_engine(connection_string)

    query = "SELECT * FROM airports"
    airports_df = pd.read_sql(query, con=engine)


    tomorrow=(datetime.now()+timedelta(days=1)).strftime('%Y-%m-%d') 
    timeslots = [('00:00','11:59'),('12:00','23:59')]
    all_flights = []

    for i, airport in airports_df.iterrows():
        icao_code = airport["icao"]

        for start, end in timeslots:
            url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{icao_code}/{tomorrow}T{start}/{tomorrow}T{end}"

            querystring = {"withLeg":"false",
                           "direction":"Both",
                           "withCancelled":"false",
                           "withCodeshared":"false",
                           "withCargo":"false",
                           "withPrivate":"false",
                           "withLocation":"false"}

            headers = {
                "x-rapidapi-key": API_key,
                "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)

            if response.status_code != 200:
                print(f"Error {response.status_code} for airport {icao_code}")
                time.sleep(2)
                continue

            arrivals = response.json().get("arrivals", [])
            if not arrivals:
                print(f"No arrivals found for {icao_code}")
                time.sleep(2)
                continue

            for flight in arrivals:
                all_flights.append({
                    "icao": airport['icao'],
                    "scheduled_arrival_time": flight.get("movement", {}).get("scheduledTime",{}).get("local"),
                    "arrival_gate": flight.get("movement", {}).get("gate"),
                    "arrival_terminal": flight.get("movement", {}).get("terminal"),
                    "icao_departure_airport": flight.get("movement", {}).get("airport",{}).get("icao"),
                    "departure_airport_name": flight.get("movement", {}).get("airport",{}).get("name")                      
                })
    all_flights_df= pd.DataFrame(all_flights)
    all_flights_df['scheduled_arrival_time']=all_flights_df['scheduled_arrival_time'].str[:-6]

    all_flights_df.to_sql(name="arrival_flights",con=connection_string, if_exists="append",index=False)

    return "Data succesfully added"
    #return pd.DataFrame(all_flights) #if all_flights else pd.DataFrame(
        #columns=["departure_airport", "departure_airport_name", "scheduled_arrival_time", "arrival_terminal", "airport_icao"])
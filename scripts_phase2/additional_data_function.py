import functions_framework
from bs4 import BeautifulSoup
import requests
import dotenv
import pandas as pd
import re
from lat_lon_parser import parse
import datetime
import pymysql
import os
from sqlalchemy import create_engine

dotenv.load_dotenv()

@functions_framework.http
def additional_data(request):
    username = os.getenv('username')
    mysql_password = os.getenv('mysql_password')
  
    schema = "gans"
    host = "34.77.218.163"
    port = 3306
   
    connection_string = f"mysql+pymysql://{username}:{mysql_password}@{host}:{port}/{schema}"
    engine = create_engine(connection_string)

    query = "SELECT * FROM cities"
    cities_df = pd.read_sql(query, con=engine)

    existing_cities = pd.read_sql("SELECT city_id FROM additional_data", con=engine)["city_id"].tolist()

    add_data = []  

    for _, row in cities_df.iterrows():
        city = row["city_name"]
        city_id = row["city_id"] 

        if city_id in existing_cities:
            continue  

        url = f'https://en.wikipedia.org/wiki/{city}'
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"Error fetching data for {city}: {response.status_code}")
            continue  

        soup = BeautifulSoup(response.content, 'html.parser')

        lat = soup.find(class_='latitude')
        lon = soup.find(class_='longitude')
        country = soup.find('th', string='Country')
        pop = soup.find(string='Population').find_next(string=re.compile(r'\d+,\d+,\d+'))

        if not (lat and lon and country and pop):
            print(f"Skipping {city}, missing some data.")
            continue  

        lat = parse(lat.text)
        lon = parse(lon.text)  
        country = country.find_next('td').text.strip()
     
        add_data.append({
            "city_id": city_id,
            #"country_name": country,
            "longitude": lon,
            "latitude": lat,
            "population": pop,
            "year_data_retrieved": datetime.now()
        })

    if add_data:
        add_data_df = pd.DataFrame(add_data)
        add_data_df.to_sql(name="additional_data", con=engine, if_exists="append", index=False)
        return "Data successfully added"
    else:
        return "No new city info add" 

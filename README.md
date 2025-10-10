# ⚡ Real-time data pipeline for Gans 🛴
 
> A practical data engineering simulation to bridge the gap between static data and dynamic urban mobility
---

## 🎯 Project Overview 

**Gans**, an e-scooter company reimagining city transport in Germany, identified two key data streams as strong revenue drivers:

- ☔️ Weather conditions directly influence ridership and fleet distribution 
- 🛬 Flight activity reveals untapped demand near airports and transit hubs
  
**But with a static database, how can real-time data be integrated to turn these insights into actions that drive revenue and efficiency?**

This project presents a real-time data engineering solution designed to make that possible. It builds an automated data pipeline that continuously collects, processes, and updates live external data — such as weather forecasts and flight information — enabling Gans to adapt its operations to dynamic city conditions.

By integrating these diverse data streams, the pipeline transforms static insights into real-time intelligence, allowing for smarter scooter deployments, optimized fleet management, and data-driven revenue growth.

In essence, this repository is a hands-on implementation of modern ETL principles and real-time analytics, turning raw data into actionable insights — and ultimately, impactful business decisions.

---
## ⚙️ Workflow

This project is divided into two main phases:

1. **Local Pipelines**
Focus: building and testing data collection and transformation processes locally.

**Steps:**

1. **Database setup (MySQL)** – Create the Gans database schema in MySQL.
2. **Data gathering** – Collect and organize external data sources.
3. **Database connection** – Connect the MySQL database with Python for ETL operations.

**2. Cloud Integration**
Focus: deploying and automating the pipeline using Google Cloud Platform (GCP) services.
  
---
## 🧰 Tech Stack 

* **Database**:MySQL Workbench
* **Programming:** Python 3.10
  * Libraries: `SQLAlchemy`,`pandas`,`requests`, `time`, `dotenv`, `functions_framework`
* **Cloud:** Google Cloud Platform (GCP)
   * Services: **Google Cloud SQL**, **Cloud Functions**, **Cloud Scheduler**

## 🧱 Project structure
```
ggans-data-pipeline/
├── scripts_phase1/               # Local pipeline scripts
│   ├── additional_df.py
│   ├── weather_df.py
│   ├── flights_airports_df.py
│
├── scripts_phase2/               # Cloud-deployed pipeline scripts
│   ├── additional_data_function.py
│   ├── weather_function.py
│   ├── flights_function.py
│   └── airports_function.py
│
├── sql/                          # Database schema & SQL queries
├── config/                       # API keys and configuration files
└── README.md
```

## 📊 Dataset & Sources

This project focuses on three major German cities: Berlin, Hamburg, and Munich

### Phase 1: Local Development

#### 🧩 1.1 Setting up the Database (MySQL)L
The schema (available in the sql/ folder) includes the following tables:

1. **cities** `city_id`, `city_name`
2. **weather:** `city_id`, `forecast_date`, `weather_desc`, `temp`, `feels_like`, `temp_min`, `temp_max`, `humidity`, `wind_speed`, `visibility`, `pop`, `rain`, `snow`, `time_retrieved`
3. **arrival_flights:** `icao`, `scheduled_arrival_time`, `arrival_gate`, `arrival_terminal`, `icao_departure_airport`, `departure_airport_name`
4. **airports:** `city_id`, `airport_name`, `icao`, `iata`, `latitude`, `longitud`
5. **additional_data:** `city_id`, `population`, `longitude`, `latitude`, `year_retrieved`

#### 🌐 1.2 Data Gathering

Sources include:

1. **Population & coordinates **– Web scraping from _Wikipedia_
2. **Weather data** – _OpenWeatherMap API_ (forecasts & current conditions)
3. **Flight data** – _AeroDataBox API_ (scheduled arrivals & departures)
4. **ICAO airport data**– _AeroDataBox_ API

Collected data is organized into Pandas DataFrames for further processing.
   
> [!IMPORTANT]
> You must subscribe to each API and store your API keys securely in a .env file.

#### 🔗 1.3 Connecting MySQL with Python

This step bridges Python and MySQL using SQLAlchemy, allowing automated data insertion, querying, and updates — the foundation of the ETL process.


---

## Others
You can read my blog about my personal experience here: 
[The Craft and Chaos of Real-Time Data Pipelines: A Hands-On Guide with Lessons Learned](https://medium.com/@laurysan0912/the-craft-and-chaos-of-real-time-data-pipelines-a-hands-on-guide-with-lessons-learned-5641919257ae)

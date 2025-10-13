# ⚡ Real-time data pipeline for Gans 🛴
 
> A practical data engineering simulation to bridge the gap between static data and dynamic urban mobility
---

## 🎯 Project Overview 

**Gans**, an e-scooter company reimagining city transport in Germany, identified two key data streams as strong revenue drivers:

- ☔️ **Weather conditions** directly influence ridership and fleet distribution 
- 🛬 **Flight activity** reveals untapped demand near airports and transit hubs
  
**But with a static database, how can real-time data be integrated to turn these insights into actions that drive revenue and efficiency?**

This project presents a real-time data engineering solution designed to make that possible. It builds an **automated data pipeline** that continuously collects, processes, and updates live external data — such as weather forecasts and flight information — enabling Gans to adapt its operations to dynamic city conditions.

By integrating these diverse data streams, the pipeline transforms static insights into real-time intelligence, allowing for smarter scooter deployments, optimized fleet management, and data-driven revenue growth.

In essence, this repository is a hands-on implementation of **ETL principles and real-time analytics**, turning raw data into actionable insights — and ultimately, impactful business decisions.

---
## ⚙️ Workflow

This project is divided into two main phases:

1. **PHASE 1: Local Pipelines**
   
   Focus: building and testing data collection and transformation processes locally.

   **Steps:**

   1. **Database setup (MySQL)** – Create the Gans database schema in MySQL.
   2. **Data gathering** – Collect and organize external data sources.
   3. **Database connection** – Connect the MySQL database with Python for ETL operations.

2. **PHASE 2: Cloud Integration**

    Focus: deploying and automating the pipeline using Google Cloud Platform (GCP) services.
  
---
## 🧰 Tech Stack 

* **Database**:MySQL Workbench
* **Programming:** Python 3.10
  * Libraries: `SQLAlchemy`,`pandas`,`requests`, `time`, `dotenv`, `functions_framework`
* **Cloud:** Google Cloud Platform (GCP)
   * Services: **Google Cloud SQL**, **Cloud Functions**, **Cloud Scheduler**

## 🧱 Project structure
```bash
gans-data-pipeline/
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
---

## 📊 Dataset & Sources

This project focuses on three major German cities: Berlin, Hamburg, and Munich

### PHASE 1: Local Development

#### 🧩 1.1 Setting up the Database (MySQL)
The schema (available in the sql/ folder) includes the following tables:
1. **cities** `city_id`, `city_name`
2. **weather:** `city_id`, `forecast_date`, `weather_desc`, `temp`, `feels_like`, `temp_min`, `temp_max`, `humidity`, `wind_speed`, `visibility`, `pop`, `rain`, `snow`, `time_retrieved`
3. **arrival_flights:** `icao`, `scheduled_arrival_time`, `arrival_gate`, `arrival_terminal`, `icao_departure_airport`, `departure_airport_name`
4. **airports:** `city_id`, `airport_name`, `icao`, `iata`, `latitude`, `longitude`
5. **additional_data:** `city_id`, `population`, `longitude`, `latitude`, `year_retrieved`

#### 🌐 1.2 Data Gathering
Sources include:
1. **Population & coordinates **– Web scraping from _Wikipedia_
2. **Weather data** – _OpenWeatherMap API_ (forecasts & current conditions)
3. **Flight data** – _AeroDataBox API_ (scheduled arrivals & departures)
4. **ICAO airport data**– _AeroDataBox_ API

Collected data is organized into Pandas DataFrames for further processing.
   
> [!IMPORTANT]
> Subscribe to each API and store your API keys securely in a `.env` file.

#### 🔗 1.3 Connecting MySQL with Python

This step bridges **Python** and **MySQL** using **SQLAlchemy**, enabling automated data insertion, querying, and updates — the foundation of the ETL process.

---

### PHASE 2: Cloud Integration

Once the local pipelines are tested and validated, the next step is to move them to the cloud for scalability, automation, and real-time performance.

The goal is to transform the local scripts into serverless functions that run automatically on Google Cloud Platform (GCP).

#### ☁️ 2.1. Architecture Overview

**1. Google Cloud SQL**
* Hosts the production database for Gans.
* Mirrors the local MySQL schema to ensure consistency between development and production.

**2. Google Cloud Functions**
* Each ETL task from Phase 1 is deployed as a separate function:
  - `additional_data_function.py` → manages demographic and location info
  - `weather_function.py` → collects and updates weather forecasts
  - `flights_function.py` → retrieves flight schedules
  - `airports_function.py` → retrieves airport data
* These functions handle data ingestion, transformation, and database updates automatically.

**3. Google Cloud Scheduler**
* Triggers the Cloud Functions at fixed intervals (e.g., hourly or daily).
* Ensures continuous data refresh without manual execution.

#### 🔄 2.2 Workflow Overview

-> Cloud Scheduler triggers the Cloud Functions on a defined schedule.
-> Each Cloud Function collects new data from sources (OpenWeatherMap, AeroDataBox, Wikipedia).
-> The data is cleaned, transformed, and loaded into Cloud SQL using SQLAlchemy.
-> The updated information becomes available for real-time insights and analysis.

This setup allows Gans to operate on live data, enabling instant adaptation to changing city conditions — a core requirement for data-driven mobility optimization.

---

## 🚀 Next Steps / Future Improvements

Looking ahead, the next phase of Gans’s data journey focuses on scaling this foundation into a production-ready ecosystem. Future enhancements could include:

* **Adding monitoring and alerting** with Google Cloud Monitoring to track data freshness, function performance, and pipeline reliability.
* **Integrating business intelligence dashboards** (e.g., Looker Studio or Tableau) to visualize real-time metrics and support data-driven decision-making.
* **Predictive Modeling** using historical and live data to train machine learning models that forecast scooter demand and optimize fleet allocation.
* **Expanding geographic and data coverage** by incorporating new cities and sources like traffic density or energy consumption for richer urban mobility insights.

These improvements would push Gans closer to a fully autonomous, insight-driven mobility platform — capable of turning every data point into smarter, faster business action.

---

## 📝 Others
You can read more about the personal experience and lessons learned while building this project in my blog:
👉[Read the full story here](https://medium.com/@laurysan0912/the-craft-and-chaos-of-real-time-data-pipelines-a-hands-on-guide-with-lessons-learned-5641919257ae)

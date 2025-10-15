/***************************
Setting up the environment
***************************/

-- Drop the database if it already exists
DROP DATABASE IF EXISTS gans;
-- ---------------------------------------

-- Create the database
CREATE DATABASE gans;
-- ---------------------------------------

-- Use the database
USE gans;

/***************************
Creating the DB Tables
***************************/

-- 1. cities---------------------------------------
CREATE TABLE cities (
    city_id INT AUTO_INCREMENT, -- Automatically generated ID for each city
    city_name VARCHAR(255) NOT NULL,
    country varchar(255) null,
    PRIMARY KEY (city_id) -- Primary key to uniquely identify each city
);

SELECT * FROM cities;

-- 2. additional_data ---------------------------------------
CREATE TABLE additional_data (
	city_id INT, -- ID of the city
	population VARCHAR(255) NOT NULL,
	longitude Decimal(10,0) Not null,
	latitude Decimal(10,0) Not null,
	year_data_retrieved DATETIME, -- Year retrtievedd
    FOREIGN KEY (city_id) REFERENCES cities(city_id) -- Foreign key to connect each city to its facts
);

Select * from additional_data;

-- 3. weather ---------------------------------------
CREATE TABLE weather (
   city_id INT,  
   forecast_date Datetime, 
   weather_desc varchar(255) not null,
   temp Decimal Not null,
   feels_like Decimal Not null,
   temp_min Decimal Not null,
   temp_max Decimal Not null,
   humidity int,
   wind_speed Decimal null,
   visibility Decimal null,
   pop Decimal null,
   rain Decimal null,
   snow Decimal null,
   time_retrieved Datetime,
   Foreign Key (city_id) References cities(city_id) -- Foreign key to connect each city to its facts
);

Select * from weather;

-- 4. airports ---------------------------------------
CREATE TABLE airports (
   city_id int,
   airport_name nvarchar(255) not null,
   icao varchar(4) not null,
   iata varchar(4) null,
   latitude decimal(10.0) not null,
   longitude decimal(10.0) not null,
   Primary key (icao),
   Foreign Key (city_id) References cities(city_id) 
);

Select * from airports;

-- 5. arrival_flights ---------------------------------------

CREATE TABLE arrival_flights (
   icao varchar(4),
   scheduled_arrival_time datetime,
   arrival_gate varchar(255) null,
   arrival_terminal int null,
   icao_departure_airport varchar(4)  NULL,
   departure_airport_name varchar(255) null,
   Foreign Key (icao) References airports(icao) 
);

Select * from arrival_flights;
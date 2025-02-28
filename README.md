# Dsc-Phase5-Project

This is a climatrack data driven pipeline for weather applications.

# CLIMATRACK - INTELLIGENT WEATHER AND CLIMATE FORECASTING
## PROJECT OVERVIEW
- A large data-driven tool called ClimaTrack was created to examine climatic trends and weather patterns.  To keep customers informed, it offers them climate reports, AI-powered forecasts, and localized weather data.

- While AI forecasts provide insights into future circumstances, users can receive real-time weather information by entering a location.  In order to assist customers in anticipating disruptions, the software also forecasts extreme weather occurrences and anomalies.

- ClimaTrack provides precise, current insights for people, researchers, and policymakers using data from NOAA and reliable weather APIs.  ClimaTrack aims to improve decision-making and readiness by providing users with accurate, data-driven insights to better comprehend and react to weather and climatic changes.

# BUSINESS UNDERSTANDING
We are attempting to address the following queries with this project:

i) How can users make better judgments about their everyday activities and long-term planning with the support of ClimaTrack's highly localized and precise weather forecasts? 

ii) How can ClimaTrack use cutting-edge AI forecasts to enhance knowledge and readiness for extreme weather events and climate anomalies? 

iii) In an increasingly climate-impacted world, how can ClimaTrack provide customized climate insights to meet the requirements of people, academics, and policymakers?


# PROBLEM STATEMENT
The need for precise, localized meteorological data, climate reports, and forecasts of extreme weather events is increasing as climate change picks up speed. 

Granular forecasts or projections pertaining to climatic anomalies are frequently absent from current solutions.

By providing comprehensive insights into weather patterns and climatic events, ClimaTrack aims to close this knowledge gap and enable users to make informed decisions and better prepare for environmental challenges.

# OBJECTIVES
a) Develop a scalable ETL pipeline to ingest, process, and analyze large-scale weather data from NOAA and weather APIs.

b) Implement machine learning models to predict localized weather trends and extreme weather events.

c) Provide interactive reports and visualizations for users to understand long-term climate trends and short-term weather anomalies.

d) Enable user-friendly access to customized weather analytics based on location inputs.

# STAKEHOLDERS
1) *Individuals*: Personalized weather insights and extreme weather alerts.

2) *Businesses & Agriculture*: Seasonal weather trend analysis for operational planning.

3) *Researchers & Environmentalists*: Access to detailed climate change trends and predictive models.

4) *Government & Disaster Management Agencies*: Proactive strategies for mitigating climate risks.

# USE CASES AND APPLICATIONS
1) *Personalized Weather Insights and notifications*: Assist people in planning their daily activities and protecting themselves against interruptions by offering them localized weather forecasts and real-time extreme weather notifications.

2) *Business & Agriculture Operational Planning*: Provide seasonal weather trend analysis to support strategic decision-making, resource optimization, and operational adjustments based on predicted weather patterns.

3)  Give academics and environmentalists access to historical climate data and predictive models so they can conduct in-depth analyses of trends in climate change and assist well-informed policymaking.

4) *Climate Risk Mitigation for Government & Disaster Management*: Provide government organizations and disaster management teams with the resources they need to create proactive climate risk plans, enhance readiness, and more skillfully handle possible climate-related calamities.

# CLIMATRACK'S COMPETITIVE ADVANTAGES
What sets climatarck apart from other solutions in the market is:

~ *Hyper-Localized Analysi*s: Unlike conventional weather apps, ClimaTrack provides location-specific trends rather than broad regional estimates.

~ *AI-Powered Anomaly Detection*: Machine learning enhances extreme weather event predictions beyond standard meteorological models.

~ *Seamless Integration*: The system can integrate with other applications via APIs for broader use cases in agriculture, insurance, and emergency response.

~ *Real-Time and Historical Data Access*:Users can compare historical patterns with real-time data to identify long-term trends.

# DATA UNDERSTANDING
In order to create a weather forecasting and anomaly detection system, we will use a variety of weather data sources.  An outline of each data component is provided below:

i) *NOAA Datasets*: - Offers historical climate data, such as temperature, precipitation, and other environmental variables, which serve as the basis for trend analysis and model training.

ii) *Third-Party Weather APIs (OpenWeather, AccuWeather, WeatherStack)*: - Provides projected and real-time weather data, improving prediction accuracy and enabling dynamic forecasting.

iii) The *ETL Process* involves extracting raw data from the previously listed sources, cleaning and normalizing it, and then loading it into a cloud-based database for effective access and storage.

# 1. Modules
1) Client
2) Frontend
3) Backend
4) Data Pipeline
5) Model

   
## Client
This is the user-facing aspect of the system. i.e simulating a user.

## Front-end
This includes html, css and js implementations

## Back-end
Implemented in python. Managing user input and acts as the service layer for that data and processes.

## Data Pipeline
This include how data is sourced, ingested, processed, and stored. Makes use of libraries such as: And technologies:

## Models
This section includes all Supervised and Unsupervised models implements using the aforementioned data.

### Preparing the data...
- It's the notepad for cleaning. Nothing fresh.
- Due to missing values and formatting mistakes, we removed them.
- To make sure the data we receive resembles the data we desire, we mapped validation functions to each of the columns.

###  Modelling:
- We modelled using a time series approach for prediction tasks (supervised) and a forest classifier for anomaly detection.(Unsupervised)
- The solution is built around a web app.
- That queries users for the geolocation information and presents them with information regarding the climatological conditions of their locale... The prevailing conditions, predictions, and anomaly detection.
- Finally, the user can be prompted to sign up and receive alerts for weather events in that locale.

~  Deployment is managed using docker.
~ Modules of the application are broken into microservices and handled by a reverse-proxy in the backend.
~ Services get called by processes in the front-end and return data to the frontend service.








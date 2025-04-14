import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import os

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Edmonton coordinates
# Edmonton, Alberta, Canada: Latitude: 53.5461, Longitude: -113.4938
latitude = 53.5461
longitude = -113.4938

# Make sure all required weather variables are listed here
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": "2020-01-01",
    "end_date": "2024-12-31",
    "daily": ["temperature_2m_max", "temperature_2m_min", "rain_sum", "precipitation_hours", "daylight_duration", "sunshine_duration"],
    "timezone": "America/Denver"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process daily data
daily = response.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
daily_rain_sum = daily.Variables(2).ValuesAsNumpy()
daily_precipitation_hours = daily.Variables(3).ValuesAsNumpy()
daily_daylight_duration = daily.Variables(4).ValuesAsNumpy()
daily_sunshine_duration = daily.Variables(5).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
    start=pd.to_datetime(daily.Time(), unit="s", utc=True),
    end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
    freq=pd.Timedelta(seconds=daily.Interval()),
    inclusive="left"
)}

daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["rain_sum"] = daily_rain_sum
daily_data["precipitation_hours"] = daily_precipitation_hours
daily_data["daylight_duration"] = daily_daylight_duration
daily_data["sunshine_duration"] = daily_sunshine_duration

daily_dataframe = pd.DataFrame(data=daily_data)
print("\nDaily data sample:")
print(daily_dataframe.head())

# Save to CSV file in the project folder
daily_csv_path = os.path.join(os.getcwd(), "edmonton_daily_weather.csv")
daily_dataframe.to_csv(daily_csv_path, index=False)

print(f"\nDaily weather data saved to: {daily_csv_path}")

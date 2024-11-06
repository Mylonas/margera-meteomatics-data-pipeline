# load packages
import datetime as dt
import meteomatics.api as api
import pandas as pd
from sqlalchemy import create_engine

# authenticate api
username = 'it_mylonas_michalis'
password = '41oTPBDn2d'

# set constant parameters
days = 6
interval_hours = 24
parameters = ['t_2m:C', 'precip_1h:mm', 'wind_speed_10m:ms']
model = 'mix'
startdate = dt.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
enddate = startdate + dt.timedelta(days=days)
interval = dt.timedelta(hours=interval_hours)

# define function for retrieving data from meteomatics
def request_data(coordinates, startdate=startdate, enddate=enddate, interval=interval,
                 parameters=parameters, username=username, password=password, model=model):
    df = api.query_time_series(coordinates,
                               startdate,
                               enddate,
                               interval,
                               parameters,
                               username,
                               password,
                               model)
    return df

# set parameters
coord_lca = [(34.923096, 33.634045)]  # larnaca
coord_ath = [(37.97945, 23.71622)]  # athens
coord_cwl = [(51.482208, -3.181301)]  # cardiff

# retrieve forecast data for each
# the following can be easily added to a loop if necessary
forecast_lca = pd.DataFrame(request_data(coord_lca)).assign(city = "larnaca")
forecast_ath = pd.DataFrame(request_data(coord_ath)).assign(city = "athens")
forecast_cwl = pd.DataFrame(request_data(coord_cwl)).assign(city = "cardiff")

# merge all data
forecasts = pd.concat([forecast_lca, forecast_ath, forecast_cwl], ignore_index=True)

# rename column for easier data manipulation
forecasts = forecasts.rename(columns={"t_2m:C": "temp",
                                      "precip_1h:mm": "precip",
                                      "wind_speed_10m:ms": "wind_speed",
                                      "city": "city"})

# Create SQLite engine
db_engine = create_engine('sqlite:///mydatabase.db')

# Store DataFrame in SQLite
forecasts.to_sql('users', con=db_engine, if_exists='replace', index=False)

# test connection between server
print(pd.read_sql('select * from users', con=db_engine))

def weekly_forecast_per_city(df, city):
    filtered_df = df[df['city'] == city]
    return filtered_df

# example for filtering by city
print(weekly_forecast_per_city(forecasts, "larnaca"))

def average_temp_of_last_week(df, city):
    filtered_df = df[df['city'] == city]
    average_temp = filtered_df['temp'].mean()
    print(f"Average temperature for the last 7 days in {city}: {average_temp:.2f}°C")
    return average_temp

# example for average temp
print(average_temp_of_last_week(forecasts, "cardiff" ))






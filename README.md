## Weather Forecast pipeline with meteomatics api

This project retrieves weather forecast data for specific cities and performs data analysis using Python. The results are stored in a SQLite database.

### Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
- [Database](#database)
- [Examples](#examples)

### Introduction

This project uses the Meteomatics API to retrieve weather forecast data (temperature, precipitation, wind speed) for Larnaca, Athens, and Cardiff. The data is processed and stored in a SQLite database for further analysis.

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/weather-forecast-analysis.git
    ```
2. Navigate to the project directory:
    ```bash
    cd weather-forecast-analysis
    ```
    
### Usage

1. **Load Packages**:
    ```python
    import datetime as dt
    import meteomatics.api as api
    import pandas as pd
    from sqlalchemy import create_engine
    ```

2. **Authenticate API**:
    ```python
    username = 'it_mylonas_michalis'
    password = '41oTPBDn2d'
    ```

3. **Set Parameters**:
    ```python
    days = 6
    interval_hours = 24
    parameters = ['t_2m:C', 'precip_1h:mm', 'wind_speed_10m:ms']
    model = 'mix'
    startdate = dt.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    enddate = startdate + dt.timedelta(days=days)
    interval = dt.timedelta(hours=interval_hours)
    ```

4. **Request Data**:
    ```python
    coord_lca = [(34.923096, 33.634045)]  # larnaca
    coord_ath = [(37.97945, 23.71622)]  # athens
    coord_cwl = [(51.482208, -3.181301)]  # cardiff

    forecast_lca = pd.DataFrame(request_data(coord_lca)).assign(city="larnaca")
    forecast_ath = pd.DataFrame(request_data(coord_ath)).assign(city="athens")
    forecast_cwl = pd.DataFrame(request_data(coord_cwl)).assign(city="cardiff")

    forecasts = pd.concat([forecast_lca, forecast_ath, forecast_cwl], ignore_index=True)

    forecasts = forecasts.rename(columns={"t_2m:C": "temp", "precip_1h:mm": "precip", "wind_speed_10m:ms": "wind_speed", "city": "city"})
    ```

### Functions

- **`request_data(coordinates, startdate, enddate, interval, parameters, username, password, model)`**: Retrieves data from Meteomatics API.
- **`weekly_forecast_per_city(df, city)`**: Filters the dataframe for the specified city.
- **`average_temp_of_last_week(df, city)`**: Calculates the average temperature for the specified city over the last week.

### Database

The project uses a SQLite database to store and retrieve the forecast data.

1. **Create SQLite Engine**:
    ```python
    db_engine = create_engine('sqlite:///mydatabase.db')
    ```

2. **Store DataFrame in SQLite**:
    ```python
    forecasts.to_sql('users', con=db_engine, if_exists='replace', index=False)
    ```

3. **Test Database Connection**:
    ```python
    print(pd.read_sql('select * from users', con=db_engine))
    ```

### Examples

- **Filter by City**:
    ```python
    print(weekly_forecast_per_city(forecasts, "larnaca"))
    ```

- **Average Temperature by city**:
    ```python
    print(average_temp_of_last_week(forecasts, "cardiff"))
    ```

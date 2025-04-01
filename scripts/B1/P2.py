from Imports import Point,Daily,pd
from main_dataset import df_merged


# Function which outputs weather features for any specified location (longitude and latitude) and period
# Define location coordinates for Disneyland Orlando (appropriate for main dataset)
latitude = 28.3772
longitude = -81.5707
altitude = None 

start_date = '2018-01-01' 
end_date = '2022-08-31'  


start = pd.to_datetime(start_date)
end = pd.to_datetime(end_date)


location = Point(latitude, longitude, altitude)

# daily weather data
weather_data = Daily(location, start, end).fetch()
# Categorizing the weather based on precipitation levels
weather_data = weather_data.fillna(0)
def categorize_weather(df):
    df["Not Rainy"] = (df["prcp"] == 0).astype(int)
    df["Rainy"] = (df["prcp"] > 0).astype(int)
    return df
weather_data = categorize_weather(weather_data)

# Ensure time is datetime and set index if not already
weather_data.index = pd.to_datetime(weather_data.index)

# Extract Year-Month
weather_data["Year_Month"] = weather_data.index.to_period("M").astype(str)

# Group by month and calculate fractions
monthly_weather_data = weather_data.groupby("Year_Month")[["Rainy", "Not Rainy"]].mean().reset_index()


# Merging fractions of rainy and non-rainy in a given month to our main dataframe
df_merged2 = pd.merge(df_merged, monthly_weather_data, on="Year_Month", how="left")

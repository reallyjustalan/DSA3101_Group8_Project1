import pandas as pd
import numpy as np
from datetime import datetime as dt
import holidays
from meteostat import Point, Daily
from sklearn.preprocessing import StandardScaler

def prepare_attendance_data(filepath):
    """Prepare attendance data from CSV file."""
    attendance_data = pd.read_csv(filepath)
    attendance_data.isnull().any()
    attendance_data.drop_duplicates(inplace=True)
    attendance_data["USAGE_DATE"] = pd.to_datetime(attendance_data["USAGE_DATE"])
    attendance_data["Year"] = attendance_data["USAGE_DATE"].dt.year
    attendance_data["Month"] = attendance_data["USAGE_DATE"].dt.month
    attendance_data["Day_of_Week"] = attendance_data["USAGE_DATE"].dt.day_name()
    
    # Handle negative attendance
    for x in attendance_data.index:
        if attendance_data.loc[x, "attendance"] < 0:
            attendance_data.loc[x, "attendance"] = 0
    
    # Standardize attendance
    attendance_data["mean_attendance"] = attendance_data.groupby(["Year", "FACILITY_NAME"])["attendance"].transform("mean")
    attendance_data["std_attendance"] = attendance_data.groupby(["Year", "FACILITY_NAME"])["attendance"].transform("std")
    attendance_data["standardized_attendance"] = (attendance_data["attendance"] - attendance_data["mean_attendance"]) / attendance_data["std_attendance"]
    
    return attendance_data

if __name__ == "__main__":
    prepare_attendance_data("data/B3/attendance.csv")

# Prepare hourly rides data from waiting_times.csv
def prepare_waiting_times(filepath):
    """Prepare waiting times data from CSV file."""
    waiting_times = pd.read_csv(filepath)
    waiting_times['DEB_TIME'] = pd.to_datetime(waiting_times['DEB_TIME'])
    waiting_times['DEB_TIME_DAY'] = waiting_times['DEB_TIME'].dt.dayofweek
    waiting_times = waiting_times[waiting_times['GUEST_CARRIED'] >= 0]
    return waiting_times[['DEB_TIME', 'DEB_TIME_DAY', 'DEB_TIME_HOUR', 'ENTITY_DESCRIPTION_SHORT', 'GUEST_CARRIED']]

if __name__ == "__main__":
    # List of file paths
    filepaths = [
        "data/B3/waiting_times_1.csv",
        "data/B3/waiting_times_2.csv",
        "data/B3/waiting_times_3.csv",
        "data/B3/waiting_times_4.csv"
    ]

    # Process and concatenate all files
    waiting_times_list = [prepare_waiting_times(fp) for fp in filepaths]
    waiting_times_combined = pd.concat(waiting_times_list, ignore_index=True)

    # Check
    print(waiting_times_combined.shape())
    print(waiting_times_combined.head())


def prepare_reserve_data(hpg_path, air_path):
    """Prepare reserve data from hpg and air CSV files."""
    hpg_reserve = pd.read_csv(hpg_path)
    hpg_reserve.drop(columns=["reserve_datetime"], inplace=True)
    hpg_reserve["visit_datetime"] = pd.to_datetime(hpg_reserve["visit_datetime"])
    hpg_reserve["hour"] = hpg_reserve["visit_datetime"].dt.hour
    hpg_hourly_sum = hpg_reserve.groupby(["hpg_store_id", "hour"])["reserve_visitors"].sum().reset_index()
    hpg_hourly_sum.rename(columns={"reserve_visitors": "sum_reserve_visitors"}, inplace=True)
    hpg_hourly_all_sum = hpg_hourly_sum.groupby("hour")["sum_reserve_visitors"].mean().reset_index()
    hpg_hourly_all_sum.rename(columns={"sum_reserve_visitors": "hpg_mean_reserve_visitors_per_hour"}, inplace=True)
    
    air_reserve = pd.read_csv(air_path)
    air_reserve.drop(columns=["reserve_datetime"], inplace=True)
    air_reserve["visit_datetime"] = pd.to_datetime(air_reserve["visit_datetime"])
    air_reserve["hour"] = air_reserve["visit_datetime"].dt.hour
    air_hourly_sum = air_reserve.groupby(["air_store_id", "hour"])["reserve_visitors"].sum().reset_index()
    air_hourly_sum.rename(columns={"reserve_visitors": "sum_reserve_visitors"}, inplace=True)
    air_hourly_all_sum = air_hourly_sum.groupby("hour")["sum_reserve_visitors"].mean().reset_index()
    air_hourly_all_sum.rename(columns={"sum_reserve_visitors": "air_mean_reserve_visitors_per_hour"}, inplace=True)
    
    return hpg_hourly_all_sum, air_hourly_all_sum

def prepare_retail_data(filepath):
    """Prepare retail data from CSV file."""
    retail_raw = pd.read_csv(filepath)
    return retail_raw[['day','hour','peak_frc']]

def prepare_park_data(filepath):
    """Prepare park data from CSV file."""
    park_raw = pd.read_csv(filepath)
    park_raw['hour_adjusted'] = park_raw['hour'] + 1
    park_daily_hourly = park_raw[['day','hour_adjusted','peak_frc']]
    park_daily_hourly["prev_peak_frc"] = park_daily_hourly.groupby("day")["peak_frc"].shift(fill_value=0)
    park_daily_hourly["peak_frc_diff"] = park_daily_hourly["peak_frc"] - park_daily_hourly["prev_peak_frc"]
    park_daily_hourly = park_daily_hourly.drop(columns=["prev_peak_frc"])
    return park_daily_hourly

def prepare_weather_data(latitude, longitude, start_date, end_date):
    """Prepare weather data using meteostat."""
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    location = Point(latitude, longitude)
    weather_data = Daily(location, start, end).fetch()
    weather_data = weather_data.fillna(0)
    weather_data["Rainy"] = (weather_data["prcp"] > 0).astype(int)
    return weather_data.reset_index()
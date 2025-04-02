import pandas as pd
from datetime import datetime as dt
from meteostat import Point, Daily

class DataPreparer:
    def __init__(self, attendance_filepath, waiting_times_filepaths, hpg_paths, air_path, retail_filepath, park_filepath, latitude, longitude, start_date, end_date):
        """Initialize file paths and parameters for data preparation."""
        self.attendance_filepath = attendance_filepath
        self.waiting_times_filepaths = waiting_times_filepaths
        self.hpg_paths = hpg_paths
        self.air_path = air_path
        self.retail_filepath = retail_filepath
        self.park_filepath = park_filepath
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date

    def prepare_attendance_data(self):
        """Prepare attendance data from CSV file."""
        attendance_data = pd.read_csv(self.attendance_filepath)
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

    def prepare_waiting_times(self):
        """Prepare waiting times data from DataFrame."""
        waiting_times_combined = pd.concat([pd.read_csv(fp) for fp in self.waiting_times_filepaths], ignore_index=True)
        waiting_times_combined['DEB_TIME'] = pd.to_datetime(waiting_times_combined['DEB_TIME'])
        waiting_times_combined['DEB_TIME_DAY'] = waiting_times_combined['DEB_TIME'].dt.dayofweek
        waiting_times_combined = waiting_times_combined[waiting_times_combined['GUEST_CARRIED'] >= 0]
        return waiting_times_combined[['DEB_TIME', 'DEB_TIME_DAY', 'DEB_TIME_HOUR', 'ENTITY_DESCRIPTION_SHORT', 'GUEST_CARRIED']]

    def prepare_reserve_data(self):
        """Prepare reserve data from hpg (2 files) and air (1 file) CSV files."""
        # Read and concatenate 2 hpg reserve files
        hpg_reserve = pd.concat([pd.read_csv(fp) for fp in self.hpg_paths], ignore_index=True)
        hpg_reserve.drop(columns=["reserve_datetime"], inplace=True)
        hpg_reserve["visit_datetime"] = pd.to_datetime(hpg_reserve["visit_datetime"])
        hpg_reserve["hour"] = hpg_reserve["visit_datetime"].dt.hour
        
        # Aggregate hpg reservations per hour
        hpg_hourly_sum = hpg_reserve.groupby(["hpg_store_id", "hour"])["reserve_visitors"].sum().reset_index()
        hpg_hourly_sum.rename(columns={"reserve_visitors": "sum_reserve_visitors"}, inplace=True)
        hpg_hourly_all_sum = hpg_hourly_sum.groupby("hour")["sum_reserve_visitors"].mean().reset_index()
        hpg_hourly_all_sum.rename(columns={"sum_reserve_visitors": "hpg_mean_reserve_visitors_per_hour"}, inplace=True)
        
        # Read air reserve file
        air_reserve = pd.read_csv(self.air_path)
        air_reserve.drop(columns=["reserve_datetime"], inplace=True)
        air_reserve["visit_datetime"] = pd.to_datetime(air_reserve["visit_datetime"])
        air_reserve["hour"] = air_reserve["visit_datetime"].dt.hour
        
        # Aggregate air reservations per hour
        air_hourly_sum = air_reserve.groupby(["air_store_id", "hour"])["reserve_visitors"].sum().reset_index()
        air_hourly_sum.rename(columns={"reserve_visitors": "sum_reserve_visitors"}, inplace=True)
        air_hourly_all_sum = air_hourly_sum.groupby("hour")["sum_reserve_visitors"].mean().reset_index()
        air_hourly_all_sum.rename(columns={"sum_reserve_visitors": "air_mean_reserve_visitors_per_hour"}, inplace=True)
        
        return hpg_hourly_all_sum, air_hourly_all_sum

    def prepare_retail_data(self):
        """Prepare retail data from CSV file."""
        retail_raw = pd.read_csv(self.retail_filepath)
        return retail_raw[['day','hour','peak_frc']]

    def prepare_park_data(self):
        """Prepare park data from CSV file."""
        park_raw = pd.read_csv(self.park_filepath)
        park_raw['hour_adjusted'] = park_raw['hour'] + 1
        park_daily_hourly = park_raw[['day','hour_adjusted','peak_frc']]
        park_daily_hourly["prev_peak_frc"] = park_daily_hourly.groupby("day")["peak_frc"].shift().fillna(0)
        park_daily_hourly["peak_frc_diff"] = park_daily_hourly["peak_frc"] - park_daily_hourly["prev_peak_frc"]
        park_daily_hourly = park_daily_hourly.drop(columns=["prev_peak_frc"])
        return park_daily_hourly

    def prepare_weather_data(self):
        """Prepare weather data using meteostat."""
        start = pd.to_datetime(self.start_date)
        end = pd.to_datetime(self.end_date)
        location = Point(self.latitude, self.longitude)
        weather_data = Daily(location, start, end).fetch()
        weather_data = weather_data.fillna(0)
        weather_data["Rainy"] = (weather_data["prcp"] > 0).astype(int)
        return weather_data.reset_index()


if __name__ == "__main__":
    # File paths for different datasets
    attendance_filepath = "data/B3/attendance.csv"
    waiting_times_filepaths = [
        "data/B3/waiting_times_1.csv",
        "data/B3/waiting_times_2.csv",
        "data/B3/waiting_times_3.csv",
        "data/B3/waiting_times_4.csv"
    ]
    hpg_paths = ["data/B3/hpg_reserve_1.csv", "data/B3/hpg_reserve_2.csv"]
    air_path = "data/B3/air_reserve.csv"
    retail_filepath = "data/B3/retail_daily_hourly.csv"
    park_filepath = "data/B3/park_daily_hourly_peaks.csv"
    latitude = 28.3772
    longitude = -81.5707
    start_date = '2018-01-01' 
    end_date = '2022-08-31'  

    data_preparer = DataPreparer(
        attendance_filepath, 
        waiting_times_filepaths, 
        hpg_paths, 
        air_path, 
        retail_filepath, 
        park_filepath, 
        latitude, 
        longitude, 
        start_date, 
        end_date
    )
    
    # Prepare data
    attendance_data = data_preparer.prepare_attendance_data()
    waiting_times_combined = data_preparer.prepare_waiting_times()
    hpg_hourly_all_sum, air_hourly_all_sum = data_preparer.prepare_reserve_data()
    retail_raw = data_preparer.prepare_retail_data()
    park_daily_hourly = data_preparer.prepare_park_data()
    weather_data = data_preparer.prepare_weather_data()

    # Outputs
    print(attendance_data.head())
    print(waiting_times_combined.head())
    print(hpg_hourly_all_sum.head())
    print(air_hourly_all_sum.head())
    print(retail_raw.head())
    print(park_daily_hourly.head())
    print(weather_data.head())
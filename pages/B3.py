import os
import sys
import streamlit as st
from pathlib import Path

# Button to trigger data preparation
if st.button("Prepare Data"):
    from data_preparation import DataPreparer  # Assuming data_preparation.py is in the correct path

    # Initialize the DataPreparer with predefined paths and parameters
    data_preparer = DataPreparer(
        attendance_filepath=attendance_filepath, 
        waiting_times_filepaths=waiting_times_filepaths, 
        hpg_paths=hpg_paths, 
        air_path=air_path, 
        retail_filepath=retail_filepath, 
        park_filepath=park_filepath, 
        latitude=latitude, 
        longitude=longitude, 
        start_date=start_date, 
        end_date=end_date
    )
    
    # Prepare the data
    attendance_data = data_preparer.prepare_attendance_data()
    waiting_times_combined = data_preparer.prepare_waiting_times()
    hpg_hourly_all_sum, air_hourly_all_sum = data_preparer.prepare_reserve_data()
    retail_raw = data_preparer.prepare_retail_data()
    park_daily_hourly = data_preparer.prepare_park_data()
    weather_data = data_preparer.prepare_weather_data()

    # Display first few rows of the prepared data for verification
    st.write("Attendance Data Sample:")
    st.write(attendance_data.head())
    st.write("Waiting Times Data Sample:")
    st.write(waiting_times_combined.head())
    st.write("HPG Hourly Reserve Data Sample:")
    st.write(hpg_hourly_all_sum.head())
    st.write("Air Hourly Reserve Data Sample:")
    st.write(air_hourly_all_sum.head())
    st.write("Retail Data Sample:")
    st.write(retail_raw.head())
    st.write("Park Data Sample:")
    st.write(park_daily_hourly.head())
    st.write("Weather Data Sample:")
    st.write(weather_data.head())
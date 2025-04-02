# sys.path.append(str(Path(file).resolve().parent.parent / 'scripts' / 'B3'))
# from data_preparation import prepare_attendance_data
 

import streamlit as st
import pandas as pd
import calendar
from data_preparation import DataPreparer
from adjusters import DemandAdjusters
from optimization_model import StaffingOptimizer
from visualization import plot_staffing

# 1. Load pre-processed data
st.title("Staffing Optimization and Visualization")

# Here we simulate that the data has already been processed in the backend
attendance_data, weather_data, reservation_data = prepare_data()

# Create Adjusters
adjusters = {
    'month_day': create_month_day_adjuster(attendance_data),
    'hour_rides': create_hourly_rides_adjuster(weather_data),
    'hour_eatery': create_hourly_eatery_adjuster(reservation_data['hpg'], reservation_data['air']),
    'hour_merch': create_hourly_merch_adjuster(reservation_data['retail']),
    'hour_general': create_hourly_general_adjuster(weather_data),
    'public_holiday': create_public_holiday_adjuster(attendance_data),
    'rain': create_rain_adjuster(weather_data)
}

# 2. Sidebar inputs for selecting month, day, rain, and public holiday
base_demand = st.number_input("Enter base demand", min_value = 1, max_value=1000000, value=10000)
month = st.sidebar.selectbox("Select Month", list(calendar.month_name[1:]))
day = st.sidebar.selectbox("Select Day of the Week", list(calendar.day_name))
rain = st.sidebar.radio("Is it raining?", ["Yes", "No"])
public_holiday = st.sidebar.radio("Is it a public holiday?", ["Yes", "No"])

rain = 1 if rain == "Yes" else 0
public_holiday = 1 if public_holiday == "Yes" else 0

# 3. Call optimization model
optimizer = StaffingOptimizer(adjusters)
staff_schedules = optimizer.optimize_staffing(month, day, rain, public_holiday)

# 4. Plot the results
st.subheader(f"Optimized Staffing for {day}, {month}")

fig = plot_staffing(staff_schedules, month, day, rain, public_holiday)
st.pyplot(fig)


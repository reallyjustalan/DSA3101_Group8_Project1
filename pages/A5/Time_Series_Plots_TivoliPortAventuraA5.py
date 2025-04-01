import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#Overview
#The Covid-19 pandemic which started in March 2020 and ended in May 2023 affected data within 
# those years as shown in the dip in 2020 and 0 attendance for some periods in 2020 and 2021. 
# It also took some time for attendance to increase to pre-pandemic levels.

def tivoli_PortAventura_overview(attendance_data):
    # Set up the plot
    plt.figure(figsize=(12, 6))

    # Plot attendance over time for each facility
    sns.lineplot(data=attendance_data, x="USAGE_DATE", y="attendance", hue="FACILITY_NAME", marker="o")

    # Beautify the plot
    plt.xlabel("Date")
    plt.ylabel("Attendance")
    plt.title("Attendance Over Time for Each Facility")
    plt.xticks(rotation=45)
    plt.legend(title="Facility Name")
    plt.grid(True)

    # Show the plot
    return plt


#Monthly Trend for each year
#Attendance from both parks follows the same trend roughly. Before Covid-19, summer break and 
# winter break periods saw an increase in attendance.

def tivoli_PortAventura_all_time(attendance_data):
    attendance_data["Year"] = attendance_data["USAGE_DATE"].dt.year
    attendance_data["Month"] = attendance_data["USAGE_DATE"].dt.month

    monthly_facility_mean = attendance_data.groupby(["Year", "Month", "FACILITY_NAME"])["attendance"].mean().reset_index()
    unique_years = monthly_facility_mean["Year"].unique()
    num_years = len(unique_years)

    fig, axes = plt.subplots(num_years, 1, figsize=(10, 5 * num_years), sharex=True, sharey=True)

    # Ensure axes is iterable even if there's only one year
    if num_years == 1:
        axes = [axes]

    # Plot each year separately
    for i, year in enumerate(sorted(unique_years)):
        ax = axes[i]
        subset = attendance_data[attendance_data["Year"] == year]  # Filter data for the current year
        
        sns.lineplot(data=subset, x="Month", y="standardized_attendance", hue="FACILITY_NAME", marker="o", ax=ax)
        
        ax.set_title(f"Attendance Trend for {year}")
        ax.set_xticks(range(1, 13))  # Ensure all months 1-12 appear on x-axis
        ax.set_xlabel("Month")
        ax.set_ylabel("standardized_attendance")
        ax.legend(title="Facility Name")
        
    return plt


#Daily trend
#Days of the week attendance data was investigated using maximum attendance per month of each
# year and mean attendance of each day. The weekends, especially Saturday saw the highest 
# attendance with both having the most count of maximum attendance days for each month of the 
# year as well as having the highest mean attendance.

#Shows which day have the most count of max attendance per month of each year
def tivoli_PortAventura_weekly_trend_max(attendance_data):
    max_attendance_per_month = attendance_data.groupby(["Year", "Month", "FACILITY_NAME"])["attendance"].max().reset_index()
    max_attendance_dates =  attendance_data.merge(max_attendance_per_month, on=["Year", "Month", "attendance"], how="inner")

    #plot day distribution
    # Count occurrences of each day in the max attendance dataset
    plt.figure(figsize=(10, 6))
    sns.countplot(data=max_attendance_dates, x="Day_of_Week", order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    # Customize the plot
    plt.xlabel("Day of the Week", fontsize=12)
    plt.ylabel("Count of Maximum Attendance Days", fontsize=12)
    plt.title("Distribution of Days with Maximum Attendance per Month", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    return plt

#Shows mean attendance trend for each day
def tivoli_PortAventura_weekly_trend_mean(attendance_data):
    # Group data by Day_of_Week and calculate mean attendance
    mean_attendance_per_day = attendance_data.groupby("Day_of_Week", as_index=False)["attendance"].mean()
    mean_attendance_per_day.rename(columns={"attendance": "mean_attendance"}, inplace=True)

    # Define the correct day order
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Convert 'Day_of_Week' to a categorical variable with the correct order
    mean_attendance_per_day["Day_of_Week"] = pd.Categorical(
        mean_attendance_per_day["Day_of_Week"], categories=day_order, ordered=True
    )

    # Sort data by ordered days
    mean_attendance_per_day = mean_attendance_per_day.sort_values("Day_of_Week")

    # Set figure size
    plt.figure(figsize=(10, 6))

    # Create bar plot
    sns.barplot(
        data=mean_attendance_per_day, 
        x="Day_of_Week", 
        y="mean_attendance", 
        order=day_order,
        palette="coolwarm"
    )

    plt.xlabel("Day of the Week", fontsize=12)
    plt.ylabel("Mean Attendance", fontsize=12)
    plt.title("Mean Attendance for Each Day of the Week", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    return plt

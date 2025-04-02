import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import holidays
from scipy.stats import ttest_ind

#Attendance on holidays are higher than on non-holidays. Holidays such as Christmas and New Years are more popular times 
#where people go to the parks.

def load_attendance_data(filepath="data/A5/cleaned_attendance.csv"):
    return pd.read_csv(filepath)

####PORT AVENTURA

#Port Aventura boxplot and stat test results holidays vs non-holidays
def port_aventura_holidays_stat_test(attendance_data):
    """
    Perform a statistical analysis with t-test and p-value to compare park attendance on holidays vs. non-holidays for Port Aventura.
    Returns a boxplot of attendance distribution.
    """

    plt.figure(figsize=(10, 6))

    #Filter for only Port Aventura
    portaventura_df = attendance_data[attendance_data["FACILITY_NAME"] == "PortAventura World"]

    #Convert to datetime
    portaventura_df["USAGE_DATE"] = pd.to_datetime(portaventura_df["USAGE_DATE"])

    #Get spain Holidays
    spain_holidays = holidays.Spain(years=[2018, 2019, 2020, 2021, 2022])
    portaventura_df["is_holiday"] = portaventura_df["USAGE_DATE"].apply(lambda x: x in spain_holidays)

    #Check average attendance on holidays
    holiday_attendance = portaventura_df[portaventura_df["is_holiday"] == True]["attendance"].mean()
    non_holiday_attendance = portaventura_df[portaventura_df["is_holiday"] == False]["attendance"].mean()

    print(f"Average attendance on holidays: {holiday_attendance}")
    print(f"Average attendance on non-holidays: {non_holiday_attendance}")

    #Use T-test and p value to see if it is statistically significant
    holiday_values = portaventura_df[portaventura_df["is_holiday"] == True]["attendance"]
    non_holiday_values = portaventura_df[portaventura_df["is_holiday"] == False]["attendance"]

    t_stat, p_value = ttest_ind(holiday_values, non_holiday_values, equal_var=False)

    print(f"T-statistic: {t_stat}, P-value: {p_value}") #p-value less than 0.05, statistically significant

    #Plot
    sns.boxplot(x=portaventura_df["is_holiday"], y=portaventura_df["attendance"])
    plt.xlabel("Public Holiday")
    plt.ylabel("Attendance")
    plt.title("Park Attendance on Public Holidays vs. Non-Holidays")

    return plt

def port_aventura_holidays_plot(attendance_data):
    """
    Generate a bar plot showing average attendance on specific holidays.
    """
    #Filter for only Port Aventura
    portaventura_df = attendance_data[attendance_data["FACILITY_NAME"] == "PortAventura World"]

    #Convert to datetime
    portaventura_df["USAGE_DATE"] = pd.to_datetime(portaventura_df["USAGE_DATE"])

    #Get Spain Holidays
    spain_holidays = holidays.Spain(years=[2018, 2019, 2020, 2021, 2022])
    portaventura_df["is_holiday"] = portaventura_df["USAGE_DATE"].apply(lambda x: x in spain_holidays)
    spain_holidays = holidays.Spain(years=portaventura_df["Year"].unique())

    # Select specific major holidays
    key_holidays = {
        "New Year's Day": "01-01",
        "Epiphany": "01-06",
        "Easter Sunday": "variable",
        "Labor Day": "05-01",
        "Christmas Day": "12-25"
    }

    # Convert variable holidays like Easter Sunday
    key_holidays["Easter Sunday"] = [date for date in spain_holidays if "Easter Sunday" in spain_holidays.get(date)]

    # Function to match holidays
    def get_holiday(date):
        date_str = date.strftime("%m-%d")
        for holiday, value in key_holidays.items():
            if isinstance(value, list) and date in value:
                return holiday
            elif date_str == value:
                return holiday
        return "Non-Holiday"

    portaventura_df["holiday_name"] = portaventura_df["USAGE_DATE"].apply(get_holiday)

    holiday_attendance = portaventura_df.groupby("holiday_name")["attendance"].mean().reset_index()
    print(holiday_attendance)

    #Plot
    plt.figure(figsize=(10, 5))
    sns.barplot(data=holiday_attendance, x="holiday_name", y="attendance", palette="viridis")

    plt.xlabel("Holiday")
    plt.ylabel("Average Attendance")
    plt.title("Park Attendance on Specific Holidays")
    plt.xticks(rotation=45)

    return plt

####TIVOLI GARDENS

def tivoli_holidays_stat_test(attendance_data):
    """
    Perform a statistical analysis with t-test and p-value to compare park attendance on holidays vs. non-holidays for Tivoli Gardens.
    Returns a boxplot of attendance distribution.
    """
    plt.figure(figsize=(10, 6))

    #Filter for only Tivoli
    tivoli_df = attendance_data[attendance_data["FACILITY_NAME"] == "Tivoli Gardens"]

    #Convert to date time
    tivoli_df["USAGE_DATE"] = pd.to_datetime(tivoli_df["USAGE_DATE"])

    #Get Denmark Holidays
    denmark_holidays = holidays.Denmark(years=[2018, 2019, 2020, 2021, 2022])
    tivoli_df["is_holiday"] = tivoli_df["USAGE_DATE"].apply(lambda x: x in denmark_holidays)

    #Check average attendance on holidays
    holiday_attendance = tivoli_df[tivoli_df["is_holiday"] == True]["attendance"].mean()
    non_holiday_attendance = tivoli_df[tivoli_df["is_holiday"] == False]["attendance"].mean()

    print(f"Average attendance on holidays: {holiday_attendance}")
    print(f"Average attendance on non-holidays: {non_holiday_attendance}")

    #Use T-test and p value to see if it is statistically significant
    holiday_values = tivoli_df[tivoli_df["is_holiday"] == True]["attendance"]
    non_holiday_values = tivoli_df[tivoli_df["is_holiday"] == False]["attendance"]

    t_stat, p_value = ttest_ind(holiday_values, non_holiday_values, equal_var=False)

    print(f"T-statistic: {t_stat}, P-value: {p_value}") #p-value less than 0.05, statistically significant

    #Plot
    sns.boxplot(x=tivoli_df["is_holiday"], y=tivoli_df["attendance"])
    plt.xlabel("Public Holiday")
    plt.ylabel("Attendance")
    plt.title("Park Attendance on Public Holidays vs. Non-Holidays")
    return plt

def tivoli_holidays_plot(attendance_data):
    """
    Generate a bar plot showing average attendance on specific holidays.
    """

    #Filter for only tivoli
    tivoli_df = attendance_data[attendance_data["FACILITY_NAME"] == "Tivoli Gardens"]

    #Convert to datetime
    tivoli_df["USAGE_DATE"] = pd.to_datetime(tivoli_df["USAGE_DATE"])

    #Find Denmark Holidays
    denmark_holidays = holidays.Denmark(years=[2018, 2019, 2020, 2021, 2022])
    tivoli_df["is_holiday"] = tivoli_df["USAGE_DATE"].apply(lambda x: x in denmark_holidays)

    denmark_holidays = holidays.Denmark(years=tivoli_df["Year"].unique())

    # Select specific major holidays
    key_holidays = {
        "New Year's Day": "01-01",
        "Easter Sunday": "variable",
        "Great Prayer Day": "variable",
        "Ascension Day": "variable",
        "Constitution Day": "06-05",
        "Christmas Eve": "12-24",
        "Christmas Day": "12-25",
        "Boxing Day": "12-26"
    }

    # Convert variable holidays (e.g., Easter Sunday, Great Prayer Day)
    variable_holidays = {}

    for date, name in denmark_holidays.items():
        holiday_name = str(name)  # Convert holiday name to a string
        if any(h in holiday_name for h in ["Easter", "Great Prayer", "Ascension"]):
            variable_holidays[holiday_name] = date

    # Add variable holidays to key_holidays
    key_holidays.update(variable_holidays)

    #Match holidays
    def get_holiday(date):
        date_str = date.strftime("%m-%d")
        for holiday, value in key_holidays.items():
            if isinstance(value, list) and date in value:
                return holiday
            elif date_str == value:
                return holiday
        return "Non-Holiday"

    tivoli_df["holiday_name"] = tivoli_df["USAGE_DATE"].apply(get_holiday)

    holiday_attendance = tivoli_df.groupby("holiday_name")["attendance"].mean().reset_index()
    print(holiday_attendance)


    plt.figure(figsize=(10, 5))
    sns.barplot(data=holiday_attendance, x="holiday_name", y="attendance", palette="viridis")

    plt.xlabel("Holiday")
    plt.ylabel("Average Attendance")
    plt.title("Park Attendance on Specific Holidays (Denmark)")
    plt.xticks(rotation=45)

    return plt


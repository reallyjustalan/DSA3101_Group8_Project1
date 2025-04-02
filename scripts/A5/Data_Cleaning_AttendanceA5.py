import pandas as pd

def attendance_data_cleaning(file_location): 
    """
    Cleans and processes attendance data containting Tivoli Garden and PortAventura
    
    Steps performed:
    1. Removes duplicate rows
    2. Converts the 'USAGE_DATE' column to datetime format
    3. Extracts 'Year', 'Month', and 'Day_of_Week' from 'USAGE_DATE'
    4. Ensures no negative values exist in the 'attendance' column and converts to 0 
    5. Computes mean and standard deviation of attendance per facility and year.
    6. Standardizes attendance values.

    """
    attendance_data = pd.read_csv(file_location)
    attendance_data.head()

    attendance_data.isnull().any() #check for null
    attendance_data.drop_duplicates(inplace = True) #drop any duplicates
    attendance_data["USAGE_DATE"] = pd.to_datetime(attendance_data["USAGE_DATE"]) #change to datetime object

    #Extract Year Month and Day of Week as columns
    attendance_data["Year"] = attendance_data["USAGE_DATE"].dt.year
    attendance_data["Month"] = attendance_data["USAGE_DATE"].dt.month
    attendance_data["Day_of_Week"] = attendance_data["USAGE_DATE"].dt.day_name()
    
    #Make sure there is no negative attendance
    for x in attendance_data.index:
        if attendance_data.loc[x, "attendance"] < 0:
            attendance_data.loc[x, "attendance"] = 0

    #mean and standard deviation of attendance per facility and year
    attendance_data["mean_attendance"] = attendance_data.groupby(["Year", "FACILITY_NAME"])["attendance"].transform("mean")
    attendance_data["std_attendance"] = attendance_data.groupby(["Year", "FACILITY_NAME"])["attendance"].transform("std")

    # Standardize attendance
    attendance_data["standardized_attendance"] = (attendance_data["attendance"] - attendance_data["mean_attendance"]) / attendance_data["std_attendance"]
    attendance_data.to_csv("data/A5/cleaned_attendance.csv")
    return attendance_data

if __name__ == "__main__":
    attendance_data_cleaning("data/A5/attendance.csv")
        
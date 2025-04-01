import pandas as pd

def attendance_data_cleaning(file_location): 
    attendance_data = pd.read_csv(file_location)
    attendance_data.head()

    attendance_data.isnull().any()
    attendance_data.drop_duplicates(inplace = True)
    attendance_data["USAGE_DATE"] = pd.to_datetime(attendance_data["USAGE_DATE"])
    attendance_data["Year"] = attendance_data["USAGE_DATE"].dt.year
    attendance_data["Month"] = attendance_data["USAGE_DATE"].dt.month
    attendance_data["Day_of_Week"] = attendance_data["USAGE_DATE"].dt.day_name()
    
    for x in attendance_data.index:
        if attendance_data.loc[x, "attendance"] < 0:
            attendance_data.loc[x, "attendance"] = 0

    attendance_data["mean_attendance"] = attendance_data.groupby(["Year", "FACILITY_NAME"])["attendance"].transform("mean")
    attendance_data["std_attendance"] = attendance_data.groupby(["Year", "FACILITY_NAME"])["attendance"].transform("std")

    # Standardize attendance
    attendance_data["standardized_attendance"] = (attendance_data["attendance"] - attendance_data["mean_attendance"]) / attendance_data["std_attendance"]
    attendance_data.to_csv("data/A5/cleaned_attendance.csv")
    return attendance_data

if __name__ == "__main__":
    attendance_data_cleaning("data/A5/attendance.csv")
        
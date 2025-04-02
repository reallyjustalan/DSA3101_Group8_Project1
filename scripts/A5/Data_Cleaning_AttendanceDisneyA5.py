import pandas as pd

def attendance_disney_data_cleaning(file_location):
    """
    Cleans and process Disney yearly attendance data 
    
    Steps performed:
    1. Strips spaces and converts the 'Attendance' column to numeric.
    2. Group the smaller parks into the main parks
    3. Groups data by 'Year' and 'Park' summing attendance values.

    """
    attendance_disney = pd.read_excel(file_location)

    #Clean Attendance Column
    attendance_disney["Attendance"] = attendance_disney["Attendance"].astype(str).str.strip()  # Remove spaces
    attendance_disney["Attendance"] = pd.to_numeric(attendance_disney["Attendance"], errors="coerce")  # Convert to numbers

    #Checking the various DisneyLands park
    unique_parks = attendance_disney["Park"].unique() 
    #DisneyLand_HongKong' 'DisneyLand Park Paris' 'Walt Disney Studios Paris' 'Disney California Adventure' 'DisneyLand Park California'

    #Group the smaller parks into the main parks
    attendance_disney["Park"] = attendance_disney["Park"].replace({"DisneyLand_Park Paris": "Disneyland_Paris", "Walt Disney Studios Paris": "Disneyland_Paris"})
    attendance_disney["Park"] = attendance_disney["Park"].replace({"Disney California Adventure": "Disneyland_California", "DisneyLand Park California": "Disneyland_California"})
    attendance_disney["Park"] = attendance_disney["Park"].replace({"DisneyLand_HongKong": "Disneyland_HongKong"})

    # Group by Year and Park, summing up attendance
    attendance_disney = attendance_disney.groupby(["Park", "Year"], as_index=False)["Attendance"].sum()
    return attendance_disney


if __name__ == "__main__":
    attendance_disney_data_cleaning("data/A5/Yearly Attendance Disney Paris Hong Kong Cali.xlsx")
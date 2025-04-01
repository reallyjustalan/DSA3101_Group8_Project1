from Imports import pd,os
from P1 import base_dir
from P5 import df_merged3

file_path = os.path.join(base_dir, "data", "B1", "events-FL-1980-2024.csv")
df_disasters_FL2 = pd.read_csv(file_path)
df_disasters_FL2 = df_disasters_FL2[['Name','Disaster','Begin Date','End Date']]
df_disasters_FL2["Begin Date"] = df_disasters_FL2["Begin Date"].astype(int)
df_disasters_FL2["End Date"] = df_disasters_FL2["End Date"].astype(int)

start_date = 20180101  # January 1, 2018
end_date = 20220831    # August 31, 2022

df_disasters_FL2_filtered = df_disasters_FL2[(df_disasters_FL2["End Date"] >= start_date) & 
                                        (df_disasters_FL2["Begin Date"] <= end_date)]
df_disasters_FL2_filtered
# Below, we merge records of the number of ongoing disasters happening in each given month and year.
df_merged3["Year_Month_dt"] = pd.to_datetime(df_merged3["Year_Month"], format="%Y-%m")
df_disasters_FL2_filtered["Begin Date"] = pd.to_datetime(df_disasters_FL2_filtered["Begin Date"], format="%Y%m%d")
df_disasters_FL2_filtered["End Date"] = pd.to_datetime(df_disasters_FL2_filtered["End Date"], format="%Y%m%d")

def count_ongoing_disasters(year_month):
    month_start = year_month  
    month_end = year_month + pd.DateOffset(days=30)  

    return ((df_disasters_FL2_filtered["Begin Date"] <= month_end) & 
            (df_disasters_FL2_filtered["End Date"] >= month_start)).sum()

df_merged3["Ongoing Disasters"] = df_merged3["Year_Month_dt"].apply(count_ongoing_disasters)
df_merged3.drop(columns=["Year_Month_dt"], inplace=True)
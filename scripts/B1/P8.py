from Imports import pd,os
from P1 import base_dir
from P7 import df_merged3

file_path = os.path.join(base_dir, "data", "B1", "attendee.csv")
df_attendee_parks = pd.read_csv(file_path)
# Filtering for records pertaining to SeaWorld Orlando and from 2018 to 2022
df_seaworld_orlando = df_attendee_parks[df_attendee_parks["name"] == "Seaworld Orlando"]
df_seaworld_orlando['Average_attendee_seaworld'] = df_seaworld_orlando['attendee_count']/12 # Data is yearly, so we derive average attendees per month
df_seaworld_orlando_filtered = df_seaworld_orlando[['year','Average_attendee_seaworld']]
df_seaworld_orlando_filtered = df_seaworld_orlando_filtered[
    (df_seaworld_orlando_filtered["year"] >= 2018) & 
    (df_seaworld_orlando_filtered["year"] <= 2022)
]

df_merged3["Year"] = df_merged3["Year_Month"].str[:4].astype(int)
df_merged3 = df_merged3.merge(df_seaworld_orlando_filtered, left_on="Year", right_on="year", how="left")
df_merged3.drop(columns=["year"], inplace=True)
df_merged3.drop(columns=["Year"], inplace=True)
# Below, performing one-hot encoding for our categorical variable "Attraction"
df_final = pd.get_dummies(df_merged3, columns=["Attraction"], drop_first=True)
attraction_columns = [col for col in df_final.columns if col.startswith("Attraction_")]
df_final[attraction_columns] = df_final[attraction_columns].astype(int)

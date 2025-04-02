from Imports import pd,os
from P1 import base_dir
from P2 import df_merged2

file_path = os.path.join(base_dir, "data", "B1", "time-series-FL-cost-1980-2024.csv")
df_disasters_FL = pd.read_csv(file_path)
df_disasters_FL_filtered = df_disasters_FL[['Year','Drought Count', 'Flooding Count', 'Freeze Count', 'Severe Storm Count', 'Tropical Cyclone Count', 'Wildfire Count','Winter Storm Count', 'All Disasters Count' ]]
# Filtering for disaster data from 2018 to 2022, to align with records in our main dataframe
df_disasters_FL_filtered = df_disasters_FL_filtered[(df_disasters_FL_filtered["Year"] >= 2018) & 
                                       (df_disasters_FL_filtered["Year"] <= 2022)]
df_merged2["Year"] = df_merged2["Year_Month"].str[:4].astype(int)
df_merged2.rename(columns={"Total_Deaths_Previous_Year": "Park_Fatalities_Previous_Year", "Not Rainy": "Fraction of Not Rainy", "Rainy": "Fraction of Rainy"}, inplace=True)
df_merged3 = pd.merge(df_merged2, df_disasters_FL_filtered, on="Year", how="left")
df_merged3.drop(columns=["Year"], inplace=True)
for col in [
    "Drought Count", "Flooding Count", "Freeze Count",
    "Severe Storm Count", "Tropical Cyclone Count",
    "Wildfire Count", "Winter Storm Count", "All Disasters Count"
]:
    df_merged3[col] = df_merged3[col] / 12 # Normalize yearly disaster counts by 12

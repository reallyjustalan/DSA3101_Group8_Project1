from Imports import pd,os
from P1 import base_dir
from P6 import df_merged3

file_path = os.path.join(base_dir, "data", "B1", "parade_night_show.xlsx")
df_parade_show = pd.read_excel(file_path)
df_parade_show = df_parade_show[['WORK_DATE','PARADE_1','PARADE_2']]
df_parade_show["Parade_Count"] = df_parade_show[["PARADE_1", "PARADE_2"]].notna().sum(axis=1)
df_parade_show["Parade_Count"] = df_parade_show["Parade_Count"].replace(0, 0)
df_parade_show=df_parade_show[['WORK_DATE','Parade_Count']]
df_parade_show["Year_Month"] = df_parade_show["WORK_DATE"].dt.to_period("M").astype(str)

# Average number of parades per month
df_avg_parades = df_parade_show.groupby("Year_Month")["Parade_Count"].mean().reset_index()
df_avg_parades.rename(columns={"Parade_Count": "Avg_no_parades"}, inplace=True)
default_parades = {}

# Setting Avg_no_parades = 2 for months before 2018-10
for year in range(2018):
    for month in range(1, 13):
        key = f"{year}-{month:02d}"
        default_parades[key] = 2.0

for month in range(1, 10):  # Jan 2018 to Sep 2018
    key = f"2018-{month:02d}"
    default_parades[key] = 2.0

# Setting Avg_no_parades = 0 for Covid-affected months (Apr 2020 - Mar 2022)
for year in [2020, 2021, 2022]:
    for month in range(1, 13):
        key = f"{year}-{month:02d}"
        if year == 2020 and month >= 4 or year in [2021] or (year == 2022 and month <= 3):
            default_parades[key] = 0.0

parades_dict = df_avg_parades.set_index("Year_Month")["Avg_no_parades"].to_dict()
parades_dict.update(default_parades)
df_merged3["Avg_no_parades"] = df_merged3["Year_Month"].map(parades_dict)
# Above, we merged the average number of night shows with our main dataframe.
# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd

# Load the latest version of daily attendance
daily_attendance_2012_2018 = kagglehub.dataset_load(
  KaggleDatasetAdapter.PANDAS,
  "ayushtankha/hackathon",
  "attendance.csv",
#   # Provide any additional arguments like 
#   # sql_query or pandas_kwargs. See the 
#   # documenation for more information:
#   # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
)

# save attendance data
pd.DataFrame(daily_attendance_2012_2018).to_csv("../data/raw/daily_attendance_2018_2022.csv", index=False)
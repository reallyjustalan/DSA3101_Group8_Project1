from Imports import pd,os
from P1 import df_yearly_deaths,base_dir

file_path = os.path.join(base_dir, "data", "B1", "waiting_times.csv")
df_attraction_details = pd.read_csv(file_path)
# Filtering for relevant variables for our dataset
df_attraction_details_filtered = df_attraction_details[['WORK_DATE', 'ENTITY_DESCRIPTION_SHORT','WAIT_TIME_MAX','NB_UNITS']]
# Below, we derive a dataframe depicting the maximum wait time for a particular attraction and the total number of people which visited it within a given month and year
df_attraction_details_filtered['WORK_DATE'] = pd.to_datetime(df_attraction_details_filtered['WORK_DATE'])
df_attraction_details_filtered['YEAR_MONTH'] = df_attraction_details_filtered['WORK_DATE'].dt.to_period('M')
df_result_attraction_details = df_attraction_details_filtered.groupby(['YEAR_MONTH', 'ENTITY_DESCRIPTION_SHORT']).agg(
    MAX_WAIT_TIME=('WAIT_TIME_MAX', 'max'),
    TOTAL_UNITS=('NB_UNITS', 'sum')
).reset_index()

df_result_attraction_details.rename(columns={'YEAR_MONTH': 'Year_Month', 'ENTITY_DESCRIPTION_SHORT': 'Attraction','MAX_WAIT_TIME': 'Max_wait_time','TOTAL_UNITS': 'Total_units' }, inplace=True)
# Below, we get the total deaths which occured in any Disney theme park in the previous year, and merge that column with our main dataframe.
df_result_attraction_details['Year_Month'] = df_result_attraction_details['Year_Month'].astype(str)
df_result_attraction_details['Year_Month'] = pd.to_datetime(df_result_attraction_details['Year_Month'])
df_result_attraction_details['Year'] = df_result_attraction_details['Year_Month'].dt.year
df_yearly_deaths['Total_Deaths_Previous_Year'] = df_yearly_deaths['Total_Deaths'].shift(1, fill_value=0)
df_merged = df_result_attraction_details.merge(
    df_yearly_deaths[['Year', 'Total_Deaths_Previous_Year']], 
    left_on='Year', 
    right_on='Year', 
    how='left'
)
df_merged = df_merged.drop(columns=['Year'])
df_merged['Year_Month'] = df_merged['Year_Month'].dt.strftime('%Y-%m')

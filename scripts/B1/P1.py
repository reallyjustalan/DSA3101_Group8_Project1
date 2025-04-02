from Imports import pd,os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Going up 3 levels to project root
file_path = os.path.join(base_dir, "data", "B1", "Disney Deadly Incidents - Total FL_CA-2.csv")
df_incidents = pd.read_csv(file_path)
df_incidents['Date of Incident'] = pd.to_datetime(df_incidents['Date of Incident'], errors='coerce')
# Filtering for deaths after and including the year 2017
df_incidents_aft_2017 = df_incidents[df_incidents['Date of Incident'].dt.year >= 2017]
df_incidents_grouped = df_incidents_aft_2017.groupby('Date of Incident').size().reset_index(name='Total_Deaths')
# Grouping fatalities by year
df_incidents_grouped['Date of Incident'] = pd.to_datetime(df_incidents_grouped['Date of Incident'])
df_yearly_deaths = (
    df_incidents_grouped.groupby(df_incidents_grouped['Date of Incident'].dt.year)['Total_Deaths']
    .sum()
    .reset_index()
    .rename(columns={'Date of Incident': 'Year'})
)

# Derived the yearly deaths on any Disney theme parks from 2017 to 2023.

from P4 import df_merged3

def determine_season(year_month):
    month = int(year_month.split('-')[1])
    if month in [3, 4, 5]:   # Spring: March - May
        return 'Spring'
    elif month in [6, 7, 8]:  # Summer: June - August
        return 'Summer'
    elif month in [9, 10, 11]: # Autumn: September - November
        return 'Autumn'
    else:                     # Winter: December - February
        return 'Winter'


df_merged3['Season'] = df_merged3['Year_Month'].apply(determine_season)
df_merged3['Spring'] = (df_merged3['Season'] == 'Spring').astype(int)
df_merged3['Summer'] = (df_merged3['Season'] == 'Summer').astype(int)
df_merged3['Autumn'] = (df_merged3['Season'] == 'Autumn').astype(int)
df_merged3['Winter'] = (df_merged3['Season'] == 'Winter').astype(int)

df_merged3.drop(columns=['Season'], inplace=True)
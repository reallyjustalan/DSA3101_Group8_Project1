from P3 import df_merged3
from Imports import pd

# Defining public holidays in Florida
public_holidays = {
    'January': ['New Year’s Day', 'Martin Luther King Jr. Day'],
    'February': ['Presidents’ Day'],
    'May': ['Memorial Day'],
    'June': ['Juneteenth'],
    'July': ['Independence Day'],
    'September': ['Labor Day'],
    'November': ['Veterans’ Day', 'Thanksgiving Day', 'Day after Thanksgiving'],
    'December': ['Christmas Day']
}

holidays_per_month = {month: len(holidays) for month, holidays in public_holidays.items()}


def count_holidays(year_month):
    month_number = int(year_month.split('-')[1])
    month_name = pd.to_datetime(f'2021-{month_number:02d}-01').strftime('%B')
    return holidays_per_month.get(month_name, 0)

df_merged3['Public_Holidays_in_Month'] = df_merged3['Year_Month'].apply(count_holidays)

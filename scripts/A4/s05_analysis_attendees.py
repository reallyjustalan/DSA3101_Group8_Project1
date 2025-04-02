import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn
from statsmodels.tsa.seasonal import seasonal_decompose, STL

dict_of_marketing_campaigns = {

    # video historical campaign: https://www.youtube.com/watch?v=jr3m7-jJBmc&ab_channel=TivoliGardens
    '175_anniversary': "2018-06-11"

}

desired_theme_park = 'PortAventura World'
daily_attendance_df = pd.read_csv('data/A4/raw/daily_attendance_2018_2022.csv', index_col='USAGE_DATE')
daily_attendance_df = daily_attendance_df.loc["2017":"2020"]
print(daily_attendance_df)
daily_attendance_df = daily_attendance_df[daily_attendance_df['FACILITY_NAME']==desired_theme_park].reset_index()
daily_attendance_df['USAGE_DATE'] = pd.to_datetime(daily_attendance_df['USAGE_DATE'])
daily_attendance_df = daily_attendance_df.set_index('USAGE_DATE')

# plt.figure(figsize=(13,13))
# plt.plot(daily_attendance_df['USAGE_DATE'], daily_attendance_df['attendance'], marker='o')

# ax= plt.gca()
# ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
# ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
# plt.xticks(rotation=45) 
# ax.set_title('Overall time series')
# ax.set_ylabel('Average visitor level / %')
# plt.show()

def get_STL_decomposition(df, desired_theme_park):
    time_series = df['attendance']
    stl = STL(time_series, seasonal=13, trend =51).fit()
    stl.plot()
    plt.suptitle(f'STL decomposition for {desired_theme_park}')
    # ax.set_ylabel('Average visitor level / %')
    plt.show()

def get_seasonal_decomposition(df, desired_theme_park):
    time_series = df['attendance']
    s_decompose = seasonal_decompose(time_series, model='multiplicative', 
                                     period=12)
    s_decompose.plot()
    plt.suptitle(f'seasonal decomposition for {desired_theme_park}')
    
    # show plot
    plt.show()
    

# get plots    
get_STL_decomposition(daily_attendance_df, desired_theme_park)
#get_seasonal_decomposition(daily_attendance_df, desired_theme_park)

# save plot
#plt.savefig(f'../other/overall_STL_decomposition.png')

# save plot
#plt.savefig(f'../other/overall_trend_time_series.png')








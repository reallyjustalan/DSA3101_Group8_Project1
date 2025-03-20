import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn
from statsmodels.tsa.seasonal import seasonal_decompose, STL

dict_of_marketing_campaigns = {

    # video historical campaign: https://www.youtube.com/watch?v=jr3m7-jJBmc&ab_channel=TivoliGardens
    '175_anniversary': "2018-06-11"

}

data = pd.read_csv('../data/raw/daily_attendance_2012_2018.csv', index_col='USAGE_DATE')
data = data.loc["2017":"2020"]
print(data)
data = data[data['FACILITY_NAME']=='PortAventura World'].reset_index()
data['USAGE_DATE'] = pd.to_datetime(data['USAGE_DATE'])
data = data.set_index('USAGE_DATE')

# plt.figure(figsize=(13,13))
# plt.plot(data['USAGE_DATE'], data['attendance'], marker='o')

# ax= plt.gca()
# ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
# ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
# plt.xticks(rotation=45) 
# ax.set_title('Overall time series')
# ax.set_ylabel('Average visitor level / %')
# plt.show()


time_series = data['attendance']
print(time_series)
stl = STL(time_series, seasonal=13).fit()
stl.plot()

# save plot
#plt.savefig(f'../other/overall_STL_decomposition.png')

# save plot
#plt.savefig(f'../other/overall_trend_time_series.png')

# show plot
plt.show()






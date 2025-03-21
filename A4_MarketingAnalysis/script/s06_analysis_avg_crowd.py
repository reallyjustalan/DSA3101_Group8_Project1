import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import seasonal_decompose, STL
from statsmodels.tsa.arima.model import ARIMA
from matplotlib.ticker import MaxNLocator
from IPython.display import HTML, display
from tabulate import tabulate

df_crowd = pd.read_csv("../data/raw/avg_crowd.csv", na_values='NA')
df_crowd['date'] = pd.to_datetime(df_crowd['year'].astype(str) + '-' + df_crowd['month'], format='%Y-%b')


df_attendee = pd.read_csv('../data/raw/attendee.csv', na_values='0')
df_attendee['date'] = pd.to_datetime(df_attendee['year'], format='%Y')

def get_hollywood_2018_yoy_growth_table_new(hollywood_df):
    hollywood_df = hollywood_df[hollywood_df['name'] == 'Disney Hollywood Studios']
    hollywood_df = hollywood_df.set_index('date')
    hollywood_df = hollywood_df.sort_index()
    hollywood_df['yoy_growth'] = (hollywood_df['attendee_count'] - hollywood_df['attendee_count'].shift(1))/hollywood_df['attendee_count']
    hollywood_df['yoy_growth'] = round(hollywood_df['yoy_growth'] * 100,1)
    hollywood_df = hollywood_df[(hollywood_df.index <= '2018') & (hollywood_df.index >= '2015')]
    hollywood_df.index = hollywood_df.index.strftime('%Y')
    hollywood_df = hollywood_df.reset_index()[['date', 'yoy_growth']]
    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    ax.table(cellText=hollywood_df.values, colLabels=hollywood_df.columns, loc='center')

    fig.tight_layout()
    display(HTML('<a id=hollywood></a>'))
    plt.show()


def get_hollywood_2018_yoy_growth_table(hollywood_df):
    hollywood_df = hollywood_df[hollywood_df['name'] == 'Disney Hollywood Studios']
    hollywood_df = hollywood_df.set_index('date')
    hollywood_df = hollywood_df.sort_index()
    hollywood_df['yoy_growth'] = (hollywood_df['attendee_count'] - hollywood_df['attendee_count'].shift(1))/hollywood_df['attendee_count']
    hollywood_df['yoy_growth'] = round(hollywood_df['yoy_growth'] * 100,1)
    hollywood_df = hollywood_df[(hollywood_df.index <= '2018') & (hollywood_df.index >= '2015')]
    hollywood_df.index = hollywood_df.index.strftime('%Y')

    return tabulate(hollywood_df[['yoy_growth']], headers=['Year','YoY Growth'], tablefmt='grid')

def get_time_series_epcot(df):
    epcot_crowd = df[df['name'] == 'Epcot']
    epcot_crowd = epcot_crowd.set_index('date')
    epcot_crowd = epcot_crowd.sort_index()
    epcot_crowd = epcot_crowd.loc['2023':'2024']
    time_series = epcot_crowd['avg_crowd_level']
    time_series.index = time_series.index.strftime('%Y %b')
    return time_series

def get_overall_time_series(time_series): 
    formatted_x_labels = time_series.index.strftime('%Y %b')
    plt.plot(formatted_x_labels, time_series.values)
    # ax.xaxis.set_major_locator(mdates.YearLocator())
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45) 
    plt.tight_layout()
    plt.show()


def get_ma_smoothed(time_series):
    s_decompose = seasonal_decompose(time_series, model='additive', 
                                     period=1 )
    
    smoothened_trend = s_decompose.trend.rolling(window=7, center=True).mean()
    plt.plot(s_decompose.trend, label='True Trend', alpha=0.5)
    plt.plot(smoothened_trend, label='Average Trend (5-MA)')
    dates= pd.date_range(start='2023-01-01', periods=12, freq='ME')
    desired_dates = ['2023 Sep', '2024 Mar']
    desired_indice = [list(time_series.index).index(desired_date) for desired_date in desired_dates]
    for index in desired_indice:
        plt.axvline(x=index,linestyle='--')
    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(nbins=14 ))
    plt.xticks(rotation=45) 
    plt.legend()
    plt.show()


def get_exp_smoothed_plot(time_series):
    smoothed_trend = time_series.ewm(alpha = 0.3, adjust=False).mean()
    plt.figure(figsize=(10,6))
    plt.plot(time_series.index, time_series, label = 'Original', alpha=0.5)
    plt.plot(smoothed_trend.index,smoothed_trend, label='Smoothed (simple exp smoothing)')
    dates= pd.date_range(start='2023-01-01', periods=12, freq='ME')
    desired_dates = ['2023 Sep', '2024 Mar']
    desired_indice = [list(time_series.index).index(desired_date) for desired_date in desired_dates]
    for index in desired_indice:
        plt.axvline(x=index,linestyle='--')
    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(nbins=14 ))
    plt.xticks(rotation=45) 
    plt.legend()
    display(HTML('<a id=EPCOT></a>'))
    plt.show()
    
# save plot
#plt.savefig(f'../other/A4_yearly_attendees_STLdecomposition.png')
plt.show()



#get_overall_time_series(epcot_crowd)    
#get_ma_smoothed(time_series)


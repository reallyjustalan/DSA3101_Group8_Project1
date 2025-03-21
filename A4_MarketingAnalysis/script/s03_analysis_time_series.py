#####################################
# author: Chris Yong Hong Sen
# date: 15 Mar 2025
# preamble: prepare time series plotting and STL decomposition plotting 
#           functions for the final notebook
# pre-req: Basic pandas and numpy manipulation functions. Basic understanding of
#          matplotlib for plotting. Date manipulation.
#
# additional notes: data cleaning  is performed in this script as well 
#           
######################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar
from statsmodels.tsa.seasonal import seasonal_decompose, STL

def plot_overall_time_series(df):
    
    fig, ax = plt.subplots(figsize = (13, 13))
    ax.plot(df['date'], df['avg_crowd_level'])

    # for year in range(min(df['date']).year + 1, max(df['date']).year):
    #     if year >= 2019:
    #         if peak_or_trough == 'peak':
    #             max_month = pd.Timestamp(year=year, month=peak_month+1, day=1)
    #             plt.axvline(x=max_month, color='orange', linestyle='--', linewidth=1)
    #         else:
    #             min_month = pd.Timestamp(year=year, month=1, day=1) 
    #             plt.axvline(x=min_month, color='orange', linestyle='--', linewidth=1)
        
    #     elif peak_or_trough == 'peak':
    #         max_month = pd.Timestamp(year=year, month=peak_month, day=1)
    #         plt.axvline(x=max_month, color='red', linestyle='--', linewidth=1)
        
    #     else:
    #         min_month = pd.Timestamp(year=year, month=trough_month, day=1)
    #         plt.axvline(x=min_month, color='red', linestyle='--', linewidth=1)
        
    plt.ylim(df['avg_crowd_level'].min()-5, df['avg_crowd_level'].max() + 5)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45) 
    ax.set_title('Overall time series')
    ax.set_ylabel('Average visitor level / %')\
        
    # save plot
    plt.savefig(f'../other/A4_yearly_attendees_time_series.png')
    
    # show plot
    plt.show()
    
    
def plot_STL_decomposition(df):
    df = df.set_index('date')
    
    stl = STL(df['avg_crowd_level'], seasonal=13).fit()
    
    stl.plot()
    
    # save plot
    plt.savefig(f'../other/A4_yearly_attendees_STLdecomposition.png')
    plt.show()

# read in data
avg_crowd_data = pd.read_csv('../data/raw/avg_crowd.csv', na_values='NA').dropna()

# prepare data for general analysis 
avg_crowd_data = avg_crowd_data.groupby(['year', 'month']).mean('avg_crowd_level').reset_index()
avg_crowd_data['month'] = avg_crowd_data['month'].apply(lambda mon: list(calendar.month_abbr).index(mon))
avg_crowd_data['date'] = pd.to_datetime(avg_crowd_data[['year', 'month']].assign(day=1))
avg_crowd_data = avg_crowd_data.loc[avg_crowd_data['date'] <= pd.Timestamp('today'), ]
avg_crowd_data = avg_crowd_data.sort_values('date').loc[avg_crowd_data['date'].dt.year >= 2015, :]



plot_overall_time_series(avg_crowd_data)
#plot_STL_decomposition(avg_crowd_data)



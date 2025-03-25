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

# used in final script
def plot_overall_avg_crowd_level(df_crowd):
    df_crowd = df_crowd.groupby('date').mean('avg_crowd_level').reset_index().sort_values('date')
    
    fig, ax = plt.subplots(figsize = (8, 6))
    ax.plot(df_crowd['date'], df_crowd['avg_crowd_level'])

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
        
    plt.ylim([0,100])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
    plt.xticks(rotation=45) 
    ax.set_title('Overall time series')
    ax.set_ylabel('Average visitor level / %')\
        
    # save plot
    #plt.savefig(f'../other/A4_yearly_attendees_time_series.png')
    
    # show plot
    plt.show()

def plot_overall_attendee_count(df):
    
    fig, ax = plt.subplots(figsize = (8, 6))
    ax.plot(df['date'], df['attendee_count'])

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
    #         plt.axvline(x=min_month, color='red', linestyle='--', linewidth=1
    
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45) 
    ax.set_title('Overall time series')
    ax.set_ylabel('Total Attendees')
        
    # save plot
    #plt.savefig(f'../other/A4_yearly_attendees_time_series.png')
    
    # show plot
    plt.show()
    
    
def plot_STL_decomposition(df):
    df = df.dropna().set_index('date')
    ts = df['avg_crowd_level']
    stl = STL(ts, period=2).fit()
    
    fig = stl.plot()
    ax = fig.axes[0]
    
    plt.xticks(rotation=45) 
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
    plt.xticks(rotation=45) 
    # save plot
    #plt.savefig(f'../other/A4_yearly_attendees_STLdecomposition.png')
    plt.show()

def plot_centered_MA_3(df, campaign_date, months_after_campaign_date):
    df = df.dropna().set_index('date')
    ts = df['avg_crowd_level']
    
    sma_centered = ts.rolling(window=3, center=True, min_periods=1).mean()
     
    fig, ax = plt.subplots(figsize = (8, 6))
    
    plt.plot(ts, label='Original Data', alpha= 0.3)
    plt.plot(sma_centered, label='Trend (3-MA)')
    plt.xlabel('Month')
    plt.ylabel('Avg Crowd Level / %')
    plt.legend()
    plt.xticks(rotation=45) 
    plt.ylim([0, 100])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
    plt.xticks(rotation=45) 
    
    # make this dynamic later
    date_after_campaign = campaign_date + pd.DateOffset(months=months_after_campaign_date)
    ax.axvline(x=date_after_campaign, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax.axvline(x=campaign_date, color='lightblue', linestyle='--', linewidth=1, alpha=0.7)
    
    plt.show()

def get_trend(df_crowd, theme_park, campaign_start_date, months_after_campaign_date):
    df_crowd = df_crowd[df_crowd['name']==theme_park].sort_values('date')
    left_date_limit = campaign_start_date - pd.DateOffset(months=6)
    right_date_limit = campaign_start_date + pd.DateOffset(months=12)
    df_crowd = df_crowd[(df_crowd['date'] >= left_date_limit) & \
                                                (df_crowd['date'] <= right_date_limit)]

    #plot_overall_attendee_count(epcot_attendee_df)
    #plot_overall_avg_crowd_level(epcot_avg_crowd_df)
    #plot_STL_decomposition(epcot_avg_crowd_df)
    plot_centered_MA_3(df_crowd, campaign_start_date, months_after_campaign_date)
    
def get_actual_data(df_crowd, theme_park, campaign_start_date, months_after_campaign_date):
    df_crowd = df_crowd[df_crowd['name']==theme_park].sort_values('date')
    left_date_limit = campaign_start_date - pd.DateOffset(months=6)
    right_date_limit = campaign_start_date + pd.DateOffset(months=12)
    df_crowd = df_crowd[(df_crowd['date'] >= left_date_limit) & \
                                                (df_crowd['date'] <= right_date_limit)]
    
    date_after_campaign = campaign_start_date + pd.DateOffset(months=months_after_campaign_date)
    
    fig, ax = plt.subplots(figsize = (8, 6))
    ax.plot(df_crowd['date'], df_crowd['avg_crowd_level'])

    ax.axvline(x=date_after_campaign, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax.axvline(x=campaign_start_date, color='skyblue', linestyle='--', linewidth=1, alpha=0.7)
    plt.ylim([0,100])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
    plt.xticks(rotation=45) 
    ax.set_title('Overall time series')
    ax.set_ylabel('Average visitor level / %')\
        
    # save plot
    #plt.savefig(f'../other/A4_yearly_attendees_time_series.png')
    
    # show plot
    plt.show()


#####################################
# author: Chris Yong Hong Sen
# date: 02 Apr 2025
# preamble: Obtain absolute and relative lifts of identified campaigns
# 
# pre-req: Intermediate understanding of pandas manipulation functions.
#
# additional notes: get_lift_of_campaign is used in s03_marketing_clustering.py
#           
######################################
import pandas as pd
from calendar import month_abbr

# Read in data
df_crowd = pd.read_csv("../data/raw/avg_crowd.csv", na_values='NA')

# Convert to datetime type  
df_crowd['date'] = pd.to_datetime(df_crowd['year'].astype(str) + '-' + \
                                        df_crowd['month'], format='%Y-%b')

def get_attraction_campaign_df(df_crowd, theme_park, campaign_date):
        """Helper function to obtain the average monthly crowd data in the 
        1. month of the campaign
        2. the month before the campaign,
        3. months of (1) and (2) in preceeding years post COVID-19 (after 2021)  

        Args:
            df_crowd (pandas.DataFrame): A monthly time series dataset of crowd 
                                        levels
            theme_park (string): A theme park that we want to obtain crowd 
                                levels from
            campaign_date (string): The date of the campaign 

        Returns:
            pandas.DataFrame: a monthly time series of crowd data with (1) to 
                                (3) achieved.
        """
        
        # convert string to datetime object
        campaign_date = pd.to_datetime(campaign_date)        

        # focus on post covid years
        dates = [2022, 2023, 2024,2025]
        
        # obtain difference in years since campaign date
        desired_year_diff = [(campaign_date.year - date) for date in dates]
        
        # only obtain years that were before campaign date
        
        # this is especially important for subsequent model training since
        # models cannot be exposed to future data (aka future years)
        # hence we are only concerned with years preceeding the campaign
        desired_year_diff = list(filter(lambda diff: diff >= 0 ,desired_year_diff))
        seasonality_campaign_dates = [(campaign_date - pd.DateOffset(years=year))\
                                        for year in desired_year_diff]
        
        # obtain the month of the campaign as well as months in preceeding years
        seasonality_after_dates = [date + pd.DateOffset(months=1) for date in \
                                        seasonality_campaign_dates]
        
        # combine the list of desired dates
        desired_dates = seasonality_campaign_dates + seasonality_after_dates

        # filter monthly crowd data the desired dates
        df_crowd = df_crowd[(df_crowd['name'] == theme_park) & \
                (df_crowd['date'].isin(desired_dates))]
        
        return df_crowd

def get_lift_of_campaign(df_crowd, theme_park, campaign_date):   
        """obtains the absolute and relative marketing lift of a campaign

        Args:
            df_crowd (pandas.DataFrame): A monthly time series dataset of crowd 
                                         levels
            theme_park (string): A theme park that we want to obtain crowd 
                                levels from
            campaign_date (string): The date of the campaign 

        Returns:
            tuple(float, float, pandas.DataFrame): A tuple of absolute marketing
                                                   lift, relative marketing 
                                                   lift, and monthly time series
                                                   pandas dataframe with
                                                   calculated absolute/marketing
                                                   as additional columns 
                                                   
        """
        
        # convert string to datetime object
        campaign_date = pd.to_datetime(campaign_date)
        
        # obtain end of campaign month and the month before campaign
        dates_for_comparison = [campaign_date, campaign_date + pd.DateOffset(months=1)]
        
        # obtain end of campaign month (1) + month before campaign (2) + 
        # months in preceeding years for (1) and (2)
        mk_df = get_attraction_campaign_df(df_crowd, theme_park, campaign_date)
        
        # Convert numerical month notation to Jan,Feb,...,Dec abbreviations
        mk_df.loc[:,'month'] = [list(month_abbr).index(month) for month in mk_df['month'].tolist()]
        
        # Calculate the seasonality during campaign months using average 
        mk_df_non_campaign_years = mk_df[~mk_df['date'].isin(dates_for_comparison)]
        avg_seasonal = mk_df_non_campaign_years.groupby('month').mean('avg_crowd_level').reset_index()
        mk_df_current = mk_df[mk_df['date'].isin(dates_for_comparison)].sort_values('month')
        mk_df_current['seasonal_avg'] = list(avg_seasonal['avg_crowd_level'])

        # Calculate the absolute influence of campaign by removing average 
        # seasonlity in preceeding years
        mk_df_current['trend_avg'] = mk_df_current['avg_crowd_level']-mk_df_current['seasonal_avg']
        absolute_lift_campaign = (mk_df_current.iloc[1,6] - mk_df_current.iloc[0,6])
        
        # Calculate the relative influence of campaign by removing average 
        # seasonlity in preceeding years
        perc_lift_campaign = round( absolute_lift_campaign / abs(mk_df_current.iloc[0,6]) * 100,1) 
        absolute_lift_campaign = round(absolute_lift_campaign, 1)
        
        
        # FOR DEBUGGING/VIEWING OUTPUTS 
        # uncomment to see the the different lifts of campaign and df of   
        # print(f'{theme_park}: {campaign_name}')
        # print('-------------------------------')
        # print(mk_df_current)
        # print('------------------------------- \n')
        # print(f'absolute lift of campaign: {absolute_lift_campaign}')
        # print(f'percentage lift of campaign: {perc_lift_campaign}%')
        
        return (absolute_lift_campaign, perc_lift_campaign, mk_df_current.iloc[0, 3])



#####################################
# author: Chris Yong Hong Sen
# date: 15 Mar 2025
# preamble: webscrape queue-times.com for attendee information for various theme
#           parks. Resultant time series related data saved as csv file in path 
#           ../data/raw/avg_crowd.csv 
# pre-req: knowledge of BeautifulSoup webscraping library and requests library 
#          for easy handling of lack of API data. Basic understanding of HTML
#          structure for a deployed website and how to access it via 'inspect'.
#          Basic pandas manipulation functions.
#
# additional notes: takes 16min (approx) to run this script. 134 parks will be 
#                   in the final dataframe 
#           
######################################

from s00_useful_functions import get_indices, check_invalid_page 
from bs4 import BeautifulSoup
import requests
import pandas as pd
        
def get_years(soup):
    """extracts the years with available data for a given theme park 

    Args:
        soup (bs4.BeautifulSoup): the entire parsed document (uncleaned)

    Returns:
        list: a list of years 
    """
    years_json = soup.find_all('div', class_='dropdown-content')[0]

    lst_of_years = years_json.find_all('a', class_= 'dropdown-item')[1:]
    url = [json.get('href') for json in lst_of_years]
    lst_of_years = [int(json.get_text()) for json in lst_of_years]
    return lst_of_years

def extract_crowd_level_table(url,year):
    """extracts name of theme park (name) for a given year (year) and month 
        (month), and the average crowd level (avg_crowd_level) for that month.

    Args:
        year (int): a specific year

    Returns:
        pd.DataFrame: A dataframe consisting of (name, year, attendee_count) 
        triplets for a given url
    """
    url = f'{url}/{year}'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    lst_of_tables = soup.find_all('table', class_='table is-fullwidth')
    
    # extract column names
    months_json = [entry for entry in lst_of_tables if entry.find('th').get_text() == 'Month'][0]
    month_time_series_columns = [col.get_text() for col in months_json.find_all('th')]
    
    # extract actual (month, avg_crowd_level) data
    months_avg_crowd_level_data = [col.get_text() for col in months_json.find_all('td')]
    month = months_avg_crowd_level_data[::2]
    avg_crowd_level = ['NA' if avg_crowd_level == '—' else avg_crowd_level for avg_crowd_level in months_avg_crowd_level_data[1::2] ] 
    
    # return a DataFrame
    data = {'name': name, 'year':year, 'month': month, 'avg_crowd_level': avg_crowd_level}
    return pd.DataFrame(data)

# initialisation
col_names = ['name', 'year', 'month', 'avg_crowd_level']
final_data = pd.DataFrame(columns=col_names)
num_of_parks = 0
accepted_indices = get_indices()
base_url = 'https://queue-times.com/parks'
for park_index in accepted_indices:
    url = f'{base_url}/{park_index}/stats'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # if no data available, skip
    if check_invalid_page(soup):
        #print(f'no data at park index: {park_index}') #uncomment for debugging 
        continue

    # name of theme park
    name = soup.find('h1', class_='title').get_text()
    name = name.split('queue')[0].split('\n')[1].strip()
    
    # get available years for current theme park
    lst_of_years = get_years(soup)
    
    # collate monthly average crowd level data for current theme park each year
    lst_of_dataframes = [extract_crowd_level_table(url, year) for year in lst_of_years] # for a theme park, get crowd level for every year data is available 
    
    # combine the data into one dataframe
    for table in lst_of_dataframes:
        final_data = pd.concat([final_data, table], ignore_index=True) 
    
    num_of_parks += 1
    print(f'number of parks added: {num_of_parks}') #uncomment for debugging

# save data as csv file
# final_data.to_csv('../data/raw/avg_crowd.csv', index=False)








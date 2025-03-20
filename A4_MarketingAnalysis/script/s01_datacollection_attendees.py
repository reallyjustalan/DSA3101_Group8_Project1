#####################################
# author: Chris Yong Hong Sen
# date: 15 Mar 2025
# preamble: webscrape queue-times.com for attendee information for various theme
#           parks. Resultant time series related data saved as csv file in path 
#           ../data/raw 
# pre-req: knowledge of BeautifulSoup webscraping library and requests library 
#          for easy handling of lack of API data. Basic understanding of HTML
#          structure for a deployed website and how to access it via 'inspect'.
#          Basic pandas manipulation functions.
#
# additional notes: takes 4 min (approx) to run this script 
#           
######################################



from useful_functions import get_indices, check_invalid_page 
from bs4 import BeautifulSoup
import requests
import pandas as pd

# get attendees time series for a given theme park
def extract_attendees_table(url):
    """extracts name of theme park (name) and number of attendees 
    (atendee_count) for a particular year (year) with the given url from 
    'queue-times.com'.

    Args:
        url (string): https://queue-times.com/{theme_park_index}/attendees

    Returns:
        pd.DataFrame: A dataframe consisting of (name, year, attendee_count) 
        triplets for a given url
    """
    response = requests.get(url) 
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # obtain theme park name
    name = soup.find('h1', class_='title').get_text()
    name = name.split('historical')[0].split('\n')[1].strip()
    
    # obtain year and attendee count
    table = soup.find("table", class_='table is-fullwidth')
    column_headers = [col.get_text() for col in table.find_all('th')]

    year_attendees_unclean = table.find_all('td')
    year = [int(year.get_text()) for year in year_attendees_unclean[::2]]
    attendee_count = [attendee.get_text() for attendee in year_attendees_unclean[1::2]]
    attendee_count = [int(attendee.split('\n')[1].replace(',','')) for attendee in attendee_count]

    # combine 
    year_attendees_clean = {'name': name, 'year': year, 'attendee_count': attendee_count}
    data = pd.DataFrame(year_attendees_clean)
    return data

num_of_parks = 0
col_names = ['name', 'year', 'attendee_count']
final_data = pd.DataFrame(columns=col_names)
accepted_indices = get_indices()

# there are only 136 parks avail
for park_index in accepted_indices:
    url = f'https://queue-times.com/parks/{park_index}/attendances'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    if check_invalid_page(soup):
        #print(f'no data at park index: {park_index}') #uncomment for debugging 
        continue

    table = extract_attendees_table(url)
    final_data = pd.concat([final_data, table], ignore_index=True)
    
    num_of_parks += 1
    print(f'number of parks added: {num_of_parks}') 

# save data as csv file
final_data.to_csv('../data/raw/attendee.csv', index=False)








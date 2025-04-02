#####################################
# author: Chris Yong Hong Sen
# date: 15 Mar 2025
# preamble: webscrape queue-times.com for valid park index. By this mode of 
#           preprocessing, we don't have to check for every indices in [1,333].
#           Resultant indices saved as txt file in path 
#           data/A4/raw/accepted_indices.txt 
# pre-req: knowledge of BeautifulSoup webscraping library and requests library 
#          for easy handling of lack of API data. Basic understanding of HTML
#          structure for a deployed website and how to access it via 'inspect'.
#
# additional notes: takes 4.5 min (approx) to run this script
#           
######################################

from bs4 import BeautifulSoup
import requests

num_of_parks = 0
park_index = 0
lst_of_accepted_indices = []
check_false_result_string = 'The page you were looking for doesn\'t exist.'

# 333 appeared to be the last index for which information was available
while park_index <= 333:
    park_index += 1
    url = f'https://queue-times.com/parks/{park_index}/'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    false_result = soup.find('h1').get_text()

    if false_result == check_false_result_string:
        continue
    
    lst_of_accepted_indices.append(park_index)
    num_of_parks += 1

print(f'Number of theme parks: {len(lst_of_accepted_indices)}')    
print(lst_of_accepted_indices)


file = open('data/A4/raw/accepted_indices.txt', 'w')

for i in lst_of_accepted_indices:
    file.write(f'{i}\n')    
file.close()

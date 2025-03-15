#####################################
# author: Chris Yong Hong Sen
# date: 15 Mar 2025
# preamble: a list of useful functions used in multiple scripts 
#           
######################################


def get_indices():
    """returns park index that is used for BeautifulSoup scraping

    Returns:
        List(int): a list of park indices 
    """
    file = open('../data/raw/accepted_indices.txt', 'r')
    indices = [int(index) for index in file.readlines()] 
    
    return indices

def check_invalid_page(soup):
    """returns either true or false if a page does not have any data

    Args:
        soup (bs4.BeautifulSoup): the entire parsed document (uncleaned)

    Returns:
        Boolean: True if no data, False if data is available
    """
    check_false_result_string = 'The page you were looking for doesn\'t exist.'
    false_result = soup.find('h1').get_text()

    return false_result == check_false_result_string
import requests
from bs4 import BeautifulSoup
import re 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import nltk
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF


def get_text_from_url(url):
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.find_all()
    title_list = soup.find_all(name='span', id='Body_Label_NewsTitle')
    title = [title_list[0].get_text()]
    
    main_text_list = soup.find_all(name='p')
    
    # removes noise (redundant recommendation from website)
    main_text = [soup.get_text() for soup in main_text_list if len(soup.find_all(name='a', target='_blank')) == 0]
    
    # removes links
    main_text = main_text[:main_text.index('Advertising')]
    return " \n".join(title + main_text)
from itertools import count

counter = count(1)

# from numba import vectorize
stop_words = set(stopwords.words('english'))
# @vectorize 
def clean_text(text, lst =[], stop_words = stop_words):
    # print(next(counter))
    # match for any length of whitespaces, change to single whitespace
    text_single_whitespace = re.sub(r'\s+', ' ', text).lower()
    
    # tokenize words: separates words from punctuations
    tokens = word_tokenize(text_single_whitespace)

    # obtain a set of stopwords
    
    stop_words.update(['place', 'line', 'experience', 'ticket', 'kid', 'disney', 'disneyland', 'time', 'ride', 'day'])
    stop_words.update(['fun', 'train', 'character', 'lot', 'attraction', 'food', 'firework', 'kid', 'ride', 'park'])
    stop_words.update(['queue', 'year', 'lot', 'character', 'ride', 'food', 'attraction', 'firework', 'kid', 'parade'])
    stop_words.update(['staff', 'visit','thing', 'land','hour', 'family', 'character', 'photo', 'attraction', 'show', 'child', 'firework', 'ride', 'minute'])
    stop_words.update(['way', 'plan', 'love', 'area', 'trip', 'price', 'adult', 'area', 'lion', 'plan', 'trip', 'people', 'water', 'weather', 'station',  'theme', 'world'])
    stop_words.update(['pass', 'part', 'weekday', 'mountain','picture', 'restaurant','mtr'])
    stop_words.update(['date', 'review_text', 'reviewer_location', 'branch', 'rating','hotel','son','app','end','age','crowd', 'bit','shop','night', 'meal'])
    stop_words.update(['grizzly', 'one', 'activity','member', 'stroller','gate', 'money','security', 'wait', 'service','adventure','group'])
    stop_words.update(['memory', 'go', 'life', 'drop','system', 'use', 'rope', 'car', 'return', 'fan','street'])
    stop_words.update(['check', 'stuff', 'holiday', 'cast','get', 'customer', 'side', 'need','hopper', 'earth', 'bag'])
    stop_words.update(['souvenir', 'cost', 'weekend', 'splash', 'reservation', 'husband', 'phone', 'option', 'birthday', 'evening'])
    stop_words.update(['morning', 'manager', 'work','spot', 'review', 'space','cut', 'entrance', 'wdw', 'baby', 'walt', 'case', 'downtown', 'week',])
    stop_words.update(['passholder', 'dining', 'tour', 'parent', 'atmosphere', 'opening', 'supervisor', 'monorail',])
    stop_words.update(['problem', 'lunch', 'access', 'min', 'friend', 'wife','view', 'sign', 'girl', 'waiting', 'issue', 'ear', 'walk',])
    stop_words.update(['point', 'entry', 'driver', 'admission', 'rest', 'daughter', 'thrill', ])
    stop_words.update(['advantage', 'schedule', 'snack', 'school', 'employee', 'parking', 'star',])
    stop_words.update(['find', 'policy', 'war', 'mickey', 'talk', 'thunder', 'disneyworld',])
    stop_words.update(['couple', 'drink', 'tip', 'guest', 'course', 'magic', 'kingdom',])
    stop_words.update(['fastpasse', 'person', 'dinner', 'mansion', 'bottle', 'see', 'light', 'summer', 'pirate',])
    stop_words.update(['book', 'party', 'choice', 'room', 'seat', 'breakfast', 'rider', 'matterhorn', 'railroad', ])
    stop_words.update(['dollar', 'break', 'shuttle', 'number', 'vacation', 'season', 'coaster', 'detail', 'afternoon',])
    stop_words.update(lst)
    # remove punctuations and stopwords
    filtered_words = [word for word in tokens if word.isalpha() and word not in stop_words]

    # loads spacy's pretrained english model in prep for lemmatization
    nlp = spacy.load('en_core_web_sm', disable=['parser'])

    # convert list of strings into a single whitespace separated single string 
    doc = nlp(' '.join(filtered_words))
    
    # return list of root word for each token
    return  (stop_words, [token.lemma_ for token in doc if token.pos_ == "NOUN" and token.lemma_ not in stop_words])

def get_topics_nmf_method(text_cleaned):    
    # initialize tfidf matrix from lemmatized text 
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(text_cleaned)

    # initialize nmf model and fit to matrix
    nmf = NMF(n_components=1, random_state=743)
    nmf.fit(tfidf)

    # return key terms for each topic
    for i, topic in enumerate(nmf.components_):
        lst = [vectorizer.get_feature_names_out()[index] for index in topic.argsort()[-10:]]
        print(f'Topic: {lst}')

    return lst



try: 
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt') 

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
    
try: 
    nltk.data.find('tokenizers/stopwords')
except LookupError:
    nltk.download('stopwords') 

# url = 'https://www.wdwmagic.com/attractions/tron/news/10jan2023-tron-lightcycle-run-announced-to-officially-open-april-4-2023-at-walt-disney-worlds-magic-kingdom.htm' 
# text = get_text_from_url(url)
# text_cleaned = clean_text(text)
# get_topics_nmf_method(text_cleaned)


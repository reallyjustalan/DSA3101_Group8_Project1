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

def clean_text(text):
    
    # match for any length of whitespaces, change to single whitespace
    #text_single_whitespace = re.sub(r'\s+', ' ', text).lower()

    # tokenize words: separates words from punctuations
    tokens = word_tokenize(text)

    # obtain a set of stopwords
    stop_words = set(stopwords.words('english'))

    # remove punctuations and stopwords
    filtered_words = [word for word in tokens if word.isalpha() and word not in stop_words]

    # loads spacy's pretrained english model in prep for lemmatization
    nlp = spacy.load('en_core_web_sm')

    # convert list of strings into a single whitespace separated single string 
    doc = nlp(' '.join(filtered_words))

    # return list of root word for each token
    return  [token.lemma_ for token in doc]

def get_topics_nmf_method(text_cleaned):    
    # initialize tfidf matrix from lemmatized text 
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(text_cleaned)

    # initialize nmf model and fit to matrix
    nmf = NMF(n_components=5, random_state=743)
    nmf.fit(tfidf)

    # return key terms for each topic
    for i, topic in enumerate(nmf.components_):
        print(f'Topic {i+1}: {[vectorizer.get_feature_names_out()[index] for index in topic.argsort()[-10:]]}')




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

url = 'https://www.wdwmagic.com/attractions/tron/news/10jan2023-tron-lightcycle-run-announced-to-officially-open-april-4-2023-at-walt-disney-worlds-magic-kingdom.htm' 
text = get_text_from_url(url)
text_cleaned = clean_text(text)

# from bertopic import BERTopic
# from bertopic.representation import KeyBERTInspired
# # from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
# from sklearn.feature_extraction.text import CountVectorizer
# from top2vec import Top2Vec  
# model = Top2Vec(text,
#                 min_count=2,
#                 speed='learn')
# _, topic_nums = model.get_topic_sizes()

# print(f'topic_nums = {topic_nums}')
# model.generate_topic_wordcloud(topic_num=0).show()
# output various modelling methods
get_topics_nmf_method(text_cleaned)


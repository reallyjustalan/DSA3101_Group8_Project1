### FAIL
### FAIL
### FAIL
### FAIL

import numpy as np
import pandas as pd

from scripts.A4.s07_campaign_nlp import clean_text, get_topics_nmf_method

df = pd.read_csv('data/A4/raw/updated_disneylandreviews.csv', encoding='latin1',
                 na_values='missing')
print(df.shape)
df_cleaned = df.dropna()
print(df_cleaned.shape)
perc_drop = round((df.shape[0] - df_cleaned.shape[0]) / df.shape[0] * 100,0)
print(f'{perc_drop}% oberservations dropped')

df_cleaned.loc[:,'date'] = pd.to_datetime(df_cleaned.loc[:,'Year_Month']) 
df_cleaned = df_cleaned.drop(['Year_Month', 'Review_ID'], axis=1)
num_of_dupes = df_cleaned[df_cleaned.duplicated()].shape[0]
total_ori = df_cleaned.shape[0]
print(f'Number of duplicates: {num_of_dupes}')
print(f'{round(num_of_dupes/total_ori * 100, 2)}% of duplicated observations dropped')
df_cleaned = df_cleaned.drop_duplicates()

# print(df_cleaned)

# import swifter
# from nltk.tokenize import word_tokenize 
# from nltk.corpus import stopwords
# import spacy
df_cleaned['Review_Text'] = df_cleaned['Review_Text'].apply(str.lower)
print(set(df_cleaned['Branch']))

df_cleaned = df_cleaned[df_cleaned['Branch'] == 'Disneyland_California']
print(df_cleaned.head(5))

def get_topics_iron_man(df_cleaned):
    #iron man debut
    df_cleaned_iron_man = df_cleaned[(df_cleaned['date'] >= '2017-01-11') & (df_cleaned['date'] <= '2017-03-31')]
    text_lst = df_cleaned_iron_man['Review_Text'].to_list()
    cleaned_text = clean_text(" \n".join(text_lst))
    print(df_cleaned_iron_man['date'].min())
    print(df_cleaned_iron_man['date'].max())
    get_topics_nmf_method(cleaned_text)

def get_topics_mickey(df_cleaned):
    # christmas mickey
    df_cleaned_mickey = df_cleaned[(df_cleaned['date'] >= '2016-11-17') & (df_cleaned['date'] <= '2016-12-31')]
    print(df_cleaned_mickey['date'].min())
    print(df_cleaned_mickey['date'].max())
    text_lst = df_cleaned_mickey['Review_Text'].to_list()
    cleaned_text = clean_text(" \n".join(text_lst))
    get_topics_nmf_method(cleaned_text)
    
def get_topics_pixar(df_cleaned):
    # christmas mickey
    df_cleaned_pixar = df_cleaned[(df_cleaned['date'] >= '2017-05-01') & (df_cleaned['date'] <= '2017-09-01')]
    print(df_cleaned_pixar['date'].min())
    print(df_cleaned_pixar['date'].max())
    text_lst = df_cleaned_pixar['Review_Text'].to_list()
    stop_words, cleaned_text = clean_text(" \n".join(text_lst))
    
    res = get_topics_nmf_method(cleaned_text)
    cond = ('guardian' in res) |  ('gardians' in res) | ('galaxy' in res) 
    while not cond:
        stop_words,cleaned_text = clean_text(" \n".join(text_lst),lst = res, stop_words=stop_words)
        res = get_topics_nmf_method(cleaned_text)
    
get_topics_pixar(df_cleaned)
# get_topics_pixar(df_cleaned)
# print('\n\nA Sparkling Christmas event: all winter')
# get_topics_mickey(df_cleaned)

# print('\n\nFirst marvel theme ride: 02 Jan 2017')   
# get_topics_iron_man(df_cleaned)

# df_cleaned['Review_Text'] = df_cleaned['Review_Text'].swifter.apply(word_tokenize)

# stop_words = set(stopwords.words('english'))
# stop_words.update(['its'])
 
# df_cleaned['Review_Text'] = df_cleaned['Review_Text'].swifter.apply(
#     lambda x: " ".join([word for word in x if word.isalpha() and word not in stop_words]) )

# print(f'FIRST ONE:\n{df_cleaned}')

# # ensure that unimportant features are disabled as it saves significant time
# nlp = spacy.load('en_core_web_sm', disable =['tagger','parser','ner','attribute_ruler','tok2vec'])
# df_cleaned['Review_Text'] = df_cleaned['Review_Text'].swifter.apply(lambda x: [token.lemma_ for token in nlp(x)])

# print(f'SECOND ONE:\n{df_cleaned}')

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.decomposition import NMF
# vectorizer = TfidfVectorizer()

# df_cleaned['vectorized'] = df_cleaned['Review_Text'].swifter.apply(lambda x: vectorizer.fit_transform(x))
# print(f'VECTORISED: {df_cleaned['vectorized'][0]}')

# # initialize nmf model and fit to matrix
# nmf = NMF(n_components=1, random_state=743, max_iter=700)
# df_cleaned['nmf_model'] = df_cleaned['vectorized'].swifter.apply(lambda x: nmf.fit(x))
# ########################
# ########################
# #######################

# # CONTINUE LATER
# #######################
# #######################
# #######################
# # return key terms for each topic
# df_cleaned['topic'] = df_cleaned['nmf_model'].swifter.apply(lambda x: x.components_[0].argsort()[::-1])

# print(df_cleaned[['Branch', 'topic']].head(5))
# df_cleaned['feature_names'] = df_cleaned.apply(lambda row: [row['vectorized'].get_feature_names_out()[i] for i in df_cleaned['topic']] ,axis=1)
# print(f'FEATURE NAME:\n{df_cleaned.head(5)}')

# df_cleaned[['Branch', 'Rating', 'date', 'Reviewer_Location', 'topic', 'feature_names']].to_csv('final.csv')
# # for i, topic in enumerate(nmf.components_):
# #     print(f'Topic {i+1}: {[vectorizer.get_feature_names_out()[index] for index in topic.argsort()[-10:]]}')

# # df_cleaned['feature_names'] =df_cleaned['vectorized'].apply(lambda x: x.get_feature_names_out()[0])
# # df_cleaned['sorted_index'] = df_cleaned['nmf_model'].apply(lambda x: x.components_[0].argsort()[::-1])
# # df_cleaned['key_words'] = [df_cleaned.loc['feature_names'][i]]

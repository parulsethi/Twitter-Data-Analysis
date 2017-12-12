import re
from nltk.corpus import stopwords
import string
import pandas
import json
import numpy as np
import plotly.offline as py
import cufflinks as cf
from textblob import TextBlob
import plotly.graph_objs as go
import folium
from folium.plugins import MarkerCluster
from gensim.parsing.preprocessing import remove_stopwords
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from scipy.misc import imread
from pymongo import MongoClient
from collections import Counter
from flask import jsonify
from pymongo import MongoClient
mongo_db_object = MongoClient("mongodb://127.0.0.1:27017/python").python
cities = ["Delhi", "Mumbai"]

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    # URLs
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')',
                       re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$',
                         re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(
            token) else token.lower() for token in tokens]
    return tokens


def clean_text(text):
    tweet = re.sub(r'https?:\/\/.*\/\w*', '', text)
    punctuation = list(string.punctuation)
    cleaned_tweet = " ".join([term for term in preprocess(tweet)
                              if term not in punctuation and
                              not term.startswith(('#', '@')) and
                              len(term) > 2])
    cleaned_tweet = cleaned_tweet.lower()
    cleaned_tweet = remove_stopwords(cleaned_tweet)
    return cleaned_tweet


def wordcloud():
    hashtags = dict()
    twitter_mask = imread('twitter_mask.png', flatten=True)
    for each_city in cities:
        hashtags[each_city] = []
        wordcloud_string = ""
        for tweet in mongo_db_object[each_city].find():

            hashtag_terms = [term for term in preprocess(tweet['text'])
                             if term.startswith('#')]
            hashtags[each_city] += hashtag_terms
            tweet_terms = " ".join(hashtag_terms)
            wordcloud_string += tweet_terms + " "

        hashtags[each_city] = Counter(hashtags).most_common(10)

        wordcloud = WordCloud(stopwords=STOPWORDS,
                              background_color='white',
                              width=5800,
                              height=5400,
                              mask=twitter_mask
                              ).generate(wordcloud_string)

        plt.imshow(wordcloud)
        plt.axis("off")
        plt.savefig(each_city + '.png', dpi=300)

    return jsonify({"tags": hashtags, "wordcloud": ""})
# plot_wordcloud(mumbai_collection)


# In[ ]:


# plot_wordcloud(delhi_collection)


# ## Top 10 users

# In[28]:

def user_histogram():
    usernames = dict()
    for each_city in cities:
        usernames[each_city] = []
        for tweet in mongo_db_object['delhi'].find():
            usernames[each_city].append(tweet['user']['name'])
        usernames[each_city] = Counter(usernames[each_city]).most_common(10)
    return jsonify({"user_histogram": usernames, "status": True})


# ## Distribution of Original Tweets vs Retweeted Tweets

# In[6]:

def tweet_status():
    retweet = dict()
    for each_city in cities:

        retweet[each_city] = 0
        for tweet in mongo_db_object[each_city].find():
            if "retweeted_status" in tweet:
                retweet[each_city] += 1
        retweet[each_city] /= mongo_db_object[each_city].count()
        retweet[each_city] = int(retweet[each_city] * 100)
    return jsonify({"retweets": retweet})

#     labels1 = ['Retweets', 'Original Tweets']
#     values1 = [mumbai_retweet, mumbai_collection.count() - mumbai_retweet]
#     labels2 = ['Retweets', 'Original Tweets']
#     values2 = [delhi_retweet, delhi_collection.count() - delhi_retweet]

# fig = {
#     "data": [
#       {
#           "values": values1,
#           "labels": labels1,
#           "domain": {"x": [0, .5]},
#           "name": "Mumbai Rains",
#           "hoverinfo":"label+percent",
#           "hole": .4,
#           "type": "pie"
#       },
#         {
#           "values": values2,
#           "labels": labels2,
#           "domain": {"x": [.5, 1]},
#           "name": "Delhi Smog",
#           "hoverinfo":"label+percent",
#           "hole": .4,
#           "type": "pie"
#       }],
#     "layout": {
#         "title": "Distribution of Original Tweets vs Retweeted Tweets",
#         "annotations": [
#             {
#                 "font": {
#                     "size": 15
#                 },
#                 "showarrow": False,
#                 "text": "Mumbai Rains",
#                 "x": 0.20,
#                 "y": 0.5
#             },
#             {
#                 "font": {
#                     "size": 15
#                 },
#                 "showarrow": False,
#                 "text": "Delhi Smog",
#                 "x": 0.8,
#                 "y": 0.5
#             }
#         ]
#     }
# }

# py.iplot(fig)


# # ## Time Series Visualisation

# # In[7]:

def tweet_time():

    data = dict()

    data['mumbai_rains'] = []
    data['mumbai_cyclone'] = []

    for tweet in mongo_db_object['Mumbai'].find():

        terms_hash = [term for term in preprocess(
            tweet['text']) if term.startswith('#')]
        # track when the hashtag is mentioned
        if '#MumbaiRains' in terms_hash:
            data['mumbai_rains'].append(tweet['created_at'])
        if '#CycloneOckhi' in terms_hash:
            data['mumbai_cyclone'].append(tweet['created_at'])

    data['delhi_smog'] = []
    data['delhi_myrightTobreathe'] = []
    data['delhi_pollution'] = []
    data['delhi_oddeven'] = []

    for tweet in mongo_db_object['Delhi'].find():
        # let's focus on hashtags only
        terms_hash = [term for term in preprocess(
            tweet['text']) if term.startswith('#')]

        if '#Smog' in terms_hash:
            data['delhi_smog'].append(tweet['created_at'])
        if '#MyRightToBreathe' in terms_hash:
            data['delhi_myrightTobreathe'].append(tweet['created_at'])
        if '#delhipollution' in terms_hash:
            data['delhi_pollution'].append(tweet['created_at'])
        if '#OddEven' in terms_hash:
            data['delhi_oddeven'].append(tweet['created_at'])

    pd = dict()
    for each_entry in data.keys():
        pd[each_entry] = pandas.Series([1] * len(data[each_entry]), index=pandas.DatetimeIndex(
            data[each_entry])).resample('D', how='sum').fillna(0)

    return jsonify({"data": data})


# # ## Network graph

# # ## Geolocations

# # In[11]:


# mumbai_locations = []
# for tweet in mumbai_collection.find():
#     if tweet['coordinates'] is not None:
#         mumbai_locations.append(tweet['coordinates']['coordinates'])

# delhi_locations = []
# for tweet in delhi_collection.find():
#     if tweet['coordinates'] is not None:
#         delhi_locations.append(tweet['coordinates']['coordinates'])

# m = folium.Map(
#     location=[18.9167, 72.8167],
#     zoom_start=5,
#     tiles='Stamen Terrain'
# )

# marker_cluster = MarkerCluster().add_to(m)

# for location in mumbai_locations:
#     folium.Marker([location[1], location[0]], icon=folium.Icon(
#         color='green')).add_to(marker_cluster)

# for location in delhi_locations:
#     folium.Marker([location[1], location[0]], icon=folium.Icon(
#         color='red')).add_to(marker_cluster)

# # m.save('locations.html')

# m


# # ## Distribution of favorite counts on Original Tweets

# # In[13]:

def user_fav():
    count = dict()

    for each_city in cities:
        count[each_city] = []
        for tweet in mongo_db_object[each_city].find():
            if "retweeted_status" not in tweet:
                count[each_city].append(int(tweet['favorite_count']))
    return jsonify({"data": count})


content_type = dict()


def tweet_type():
    for each_city in cities:

        content_type[each_city] = dict()

        for each_content_type in ["text", "image", "text_image"]:
            content_type[each_city][each_content_type] = 0

        for tweet in mongo_db_object[each_city].find():
            if "media" in tweet["entities"]:
                for x in tweet["entities"]["media"]:
                    if x["type"] == "photo":
                        if tweet['text']:
                            content_type[each_city]["text_image"] += 1
                        else:
                            content_type[each_city]["image"] += 1
                        break
            else:
                content_type[each_city]['text'] += 1

    return jsonify({"data": content_type})


def tweet_rescue():

    scheme_type = "odd_even"
    city_of_operation = "Delhi"
    values = dict()
    values[city_of_operation] = dict()
    values[city_of_operation][scheme_type] = []

    for tweet in mongo_db_object[city_of_operation].find():
        if '#OddEven' in preprocess(tweet['text']):
            values[city_of_operation][scheme_type].append(
                clean_text(tweet['text']))

    sentiment = dict()
    sentiment['+'] = 0
    sentiment['-'] = 0
    sentiment['.'] = 0

    for tweet in values[city_of_operation][scheme_type]:
        polarity = TextBlob(tweet).sentiment.polarity
        if polarity > 0.0:
            sentiment['+'] += 1
        elif polarity == 0:
            sentiment['-'] += 1
        else:
            sentiment['.'] += 1
    total = sentiment['+'] + sentiment['.'] + sentiment['-']
    sentiment['+'] /= total
    sentiment['.'] /= total
    sentiment['-'] /= total
    return jsonify({"data": sentiment})


# import gensim
# import pyLDAvis.gensim

# from gensim.models import LdaModel
# from gensim.corpora import Dictionary

# cleaned_text_mumbai = []
# cleaned_text_delhi = []

# for tweet in mumbai_collection.find():
#     cleaned_text_mumbai.append(clean_text(tweet['text']).split())

# for tweet in delhi_collection.find():
#     cleaned_text_delhi.append(clean_text(tweet['text']).split())

# # create dictionary mappings for training data
# mumbai_dictionary = Dictionary(cleaned_text_mumbai)
# delhi_dictionary = Dictionary(cleaned_text_delhi)

# # create corpus using training data's dictionary mappings
# mumbai_corpus = [mumbai_dictionary.doc2bow(
#     text) for text in cleaned_text_mumbai]
# delhi_training_corpus = [delhi_dictionary.doc2bow(
#     text) for text in cleaned_text_delhi]


# # In[4]:


# # train LDA model
# mumbai_lda_model = LdaModel(corpus=mumbai_corpus, id2word=mumbai_dictionary,
#                             num_topics=10, passes=50, chunksize=1500, iterations=200, alpha='auto')
# delhi_lda_model = LdaModel(corpus=training_corpus, id2word=dictionary,
# num_topics=10, passes=50, chunksize=1500, iterations=200, alpha='auto')


# # In[5]:


# pyLDAvis.enable_notebook()
# pyLDAvis.gensim.prepare(mumbai_lda_model, mumbai_corpus,
#                         mumbai_dictionary, sort_topics=False)


# # In[ ]:


# pyLDAvis.gensim.prepare(delhi_lda_model, delhi_training_corpus,
#                         delhi_dictionary, sort_topics=False)

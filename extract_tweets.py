
import json
import re
import tweepy
import json
import time
from pymongo import MongoClient

#Twitter API credentials
consumer_key = 'my-consumer-key'
consumer_secret = 'my-consumer-secret'
access_key = 'my-access-key'
access_secret = 'my-access-secret'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# search term
mumbai_rain_keywords = '#MumbaiRains OR #CycloneOckhi'
delhi_pollution_keywords = '#smog OR #OddEven OR #letdelhibreathe OR #delhiairpollution OR #DelhiChokes OR #letdelhibreathe OR #DelhiGasChamber OR #delhismog OR #smogindelhi OR #delhipollution OR #cropburning OR #myrighttobreathe'

users = tweepy.Cursor(api.search, q=mumbai_rain_keywords, lang="en", include_entities=True).items()
count = 0
errorCount=0

client = MongoClient()

delhi_db = client['delhi_db']
delhi_collection = db['delhi_collection']
mumbai_db = client['mumbai_db']
mumbai_collection = db['mumbai_collection']

while True:
    try:
        user = next(users)
        count += 1
        if (count>100):
           break
    except tweepy.TweepError:
        print("sleeping....")
        time.sleep(60*16)
        user = next(users)
    except StopIteration:
        break
    try:
        mumbai_collection.insert(user._json)
        
    except UnicodeEncodeError:
        errorCount += 1
        print("UnicodeEncodeError,errorCount ="+str(errorCount))
    

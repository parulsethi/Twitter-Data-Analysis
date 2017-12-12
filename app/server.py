import RAKE
from nltk.stem.wordnet import WordNetLemmatizer
from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from nltk.corpus import wordnet as wn
from pymongo import MongoClient
import difflib
from bson.objectid import ObjectId
from bson import json_util
from datetime import date, datetime
import numpy as np
from numpy import random
import Twitter_analysis

url = "mongodb://127.0.0.1:27017/python"

# database_referencer = parse_Object(url)
# feed_generator = feed(url, database_referencer)
# user_preferences = preferences()

app = Flask(__name__)
CORS(app)

app.route("/user/histogram")(Twitter_analysis.user_histogram)
app.route("/word/cloud")(Twitter_analysis.wordcloud)
app.route("/tweet/status")(Twitter_analysis.tweet_status)
app.route("/tweet/time")(Twitter_analysis.tweet_time)
app.route("/user/fav")(Twitter_analysis.user_fav)
app.route("/tweet/media_type")(Twitter_analysis.tweet_type)
app.route("/tweet/sentiment")(Twitter_analysis.tweet_rescue)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2003, threaded=True, debug=True)

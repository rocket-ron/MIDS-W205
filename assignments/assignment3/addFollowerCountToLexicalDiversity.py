from pymongo import MongoClient
import tweepy
import twitterAuth
import time
import sys

# This little program takes the lexdiv collection from the db_restT database and
# adds a new field for the follower_count for the Twitter user id. The resulting
# document is stored in a new collection called lexdiv2


mongoClient = MongoClient('192.168.194.171', port=27017)
db = mongoClient.db_restT

auth = twitterAuth.getAppAuth('W205_A3F')
api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

docs = db.lexdiv.find()
for doc in docs:
    del doc['_id']
    doc['followers_count']=api.get_user(user_id=doc['user_id']).followers_count
    db.lexdiv2.insert_one(doc)
    time.sleep(5)

mongoClient.close()
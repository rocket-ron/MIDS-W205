#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 12:54:19 2015

@author: nicholashamlin
"""

import pymongo

def get_from_mongo(term,count):
    conn=pymongo.MongoClient(host='54.153.43.230',port=27017)
    tweets = conn['twitter_db'][term]
    predict_tweets=(tweets.find().limit(count))
    return predict_tweets #returns a cursor now, not a list

if __name__=='__main__':
    tweets=get_from_mongo('isis',10) 
    for tweet in iter(tweets):
        try:
            print tweet['text']+"<split>"+tweet['user']['screen_name']+"<split>"+str(tweet['user']['followers_count'])
        except UnicodeEncodeError:
            continue

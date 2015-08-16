#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 19:03:10 2015

@author: nicholashamlin
"""

import pickle
import re

from mrjob.job import MRJob
from datetime import datetime
from mrjob.protocol import JSONProtocol, JSONValueProtocol

from boto.s3.connection import S3Connection
from boto.s3.key import Key
conn = S3Connection(host="s3-us-west-1.amazonaws.com")
bucket = conn.get_bucket('w205-rcordell-project')
f_key = bucket.get_key('emr/classifier.pkl')
v_key = bucket.get_key('emr/vectorizer.pkl')
tlc = pickle.loads(f_key.get_contents_as_string())
vec = pickle.loads(v_key.get_contents_as_string())

"""

When reading the pickle files from a local store use the
code below.


with open("classifier.pkl","rb") as f:
    tlc=pickle.load(f)
with open("vectorizer.pkl","rb") as v:
    vec=pickle.load(v)
"""

def predict_one (predict_tweet,trained_classifier, vectorizer):
    predict_data=[predict_tweet]
    predict_vectors = vectorizer.transform(predict_data)
    prediction=trained_classifier.predict(predict_vectors)
    return prediction
        
class MRFearTweetCount(MRJob):

    INPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, tweet):
        self.increment_counter('group_1', 'total_tweets', 1)
        if 'user' in tweet and 'text' in tweet and 'created_at' in tweet:
            text = tweet['text']
            user = tweet['user']['id_str']
            date_str = (tweet['created_at']).replace("+0000 ","")
            date = datetime.strptime(date_str,"%a %b %d %H:%M:%S %Y").strftime("%x")
            emotion = predict_one(text, tlc, vec)
            if emotion == 'fear':
                yield date,1
            else:
                yield date,0

    def reducer(self, key, values):
        val,count=0,0
        # gotta write an aggregator to both count and add values at the same time
        for i in values:
            count += 1
            val += i     
        yield key, val/float(count)

if __name__ == '__main__':
    MRFearTweetCount.run()

#To run locally:
#Simple version: ./fear_count.py test.csv

#To run on EMR:
#python fear_timeseries.py -r emr --conf-path mrjob.conf s3://hamlin-mids-mapreduce/input/test.csv

#python fear_timeseries.py -r emr --no-output --output-file s3://w205-rcordell-project/emr/fearcounts --conf-path mrjob.conf s3://w205-rcordell-project/emr/data/ebola.json

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 19:03:10 2015

@author: nicholashamlin
"""

import pickle


from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, JSONValueProtocol

"""

Use the boto module code to fetch the pickle files from S3 

"""

from boto.s3.connection import S3Connection
from boto.s3.key import Key
conn = S3Connection(host="s3-us-west-1.amazonaws.com")
bucket = conn.get_bucket('w205-rcordell-project')
f_key = bucket.get_key('emr/classifier.pkl')
v_key = bucket.get_key('emr/vectorizer.pkl')
tlc = pickle.loads(f_key.get_contents_as_string())
vec = pickle.loads(v_key.get_contents_as_string())

"""

Use this code to open a local pickle file to feed into the model
If you use this with AWS EMR you must make sure the pickle files
are uploaded to the hadoop user directory.

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
            if 'user' in tweet and 'text' in tweet and 'followers_count' in tweet['user']:
                text=tweet['text']
                user=tweet['user']['id_str']
                followers=int(tweet['user']['followers_count'])
                emotion=predict_one(text,tlc,vec)
                if emotion=='fear':
                    yield user,followers

    def reducer(self, key, values):
        total=sum(values)
        yield key, total

if __name__ == '__main__':
    MRFearTweetCount.run()

#To run locally:
#Simple version: ./fear_count.py test.csv

#To run on EMR:
#python fear_count.py -r emr --no-output --output-file s3://w205-rcordell-project/emr/fearcounts --conf-path mrjob.conf s3://w205-rcordell-project/emr/data/ebola.json

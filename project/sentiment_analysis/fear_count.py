#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 19:03:10 2015

@author: nicholashamlin
"""

import pickle


from mrjob.job import MRJob
from mrjob.step import MRStep
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

    def mapper_get_fear_counts(self, _, tweet):
        self.increment_counter('group_1', 'total_tweets', 1)
        if 'user' in tweet and 'text' in tweet and 'followers_count' in tweet['user']:
            text=tweet['text']
            user=tweet['user']['id_str']
            followers=int(tweet['user']['followers_count'])
            emotion=predict_one(text,tlc,vec)
            if emotion=='fear':
                self.increment_counter('group_1', 'fear_tweets', 1)
                yield user,followers

    def combiner_count_fear(self, key, values):
        yield key, sum(values)

    def reducer_count_fear(self, user, count):
        yield None, (sum(count), user)

    def sort_counts(self, _, counts):
        yield None, sorted(counts, reverse=True)

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_fear_counts,
                   combiner=self.combiner_count_fear,
                   reducer=self.reducer_count_fear),
            MRStep(reducer=self.sort_counts)]

if __name__ == '__main__':
    MRFearTweetCount.run()

#To run locally:
#Simple version: ./fear_count.py test.csv
# To gather from Mongo: python ./get_tweets.py | python ./fear_count.py > test_data.csv

#To run on EMR:
#python fear_count.py -r emr --no-output --output-file s3://w205-rcordell-project/emr/fearcounts --conf-path mrjob.conf s3://w205-rcordell-project/emr/data/ebola.json

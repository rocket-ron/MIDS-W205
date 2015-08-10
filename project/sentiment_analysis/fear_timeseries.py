#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 19:03:10 2015

@author: nicholashamlin
"""

import pickle

from mrjob.job import MRJob
from datetime import datetime

with open("classifier.pkl","rb") as f:
    tlc=pickle.load(f)
with open("vectorizer.pkl","rb") as v:
    vec=pickle.load(v)
    
def predict_one (predict_tweet,trained_classifier, vectorizer):
    predict_data=[predict_tweet]
    predict_vectors = vectorizer.transform(predict_data)
    prediction=trained_classifier.predict(predict_vectors)
    return prediction
        
class MRFearTweetCount(MRJob):

    def mapper(self, _, line):
        if line.find('<split>')>0:
            tweet=line.split("<split>")
            text=tweet[0]
            user=tweet[1]
            date=datetime.strptime(tweet[3],"%c").strftime("%x")
            emotion=predict_one(text,tlc,vec)
            if emotion=='fear':
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
#python fear_count.py -r emr --conf-path mrjob.conf s3://hamlin-mids-mapreduce/input/test.csv

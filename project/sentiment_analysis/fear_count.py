#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 19:03:10 2015

@author: nicholashamlin
"""

import pickle

from mrjob.job import MRJob

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
            followers=int(tweet[2])
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
#python fear_count.py -r emr --conf-path mrjob.conf s3://hamlin-mids-mapreduce/input/test.csv

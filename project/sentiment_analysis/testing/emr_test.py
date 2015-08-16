#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 19:03:10 2015

@author: nicholashamlin
"""

import re

from mrjob.job import MRJob
import sklearn

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        """Parse tweets from input, remove non-alphanumeric characters
        and return key,value pair for each word"""
        tweet=line.split(",")[1].lower()
        tweet=re.sub(r'[^a-z 0-9]','', tweet)
        words=tweet.split()
        for word in words:
            yield word, 1

    def reducer(self, key, values):
        """Aggregate total instances of words, and only return those that appear
        more than 10,000 times"""
        total=sum(values)
        if total>10000: #put cutoff here
            yield key, total

if __name__ == '__main__':
    MRWordFrequencyCount.run()

#To run locally:
#Simple version: ./emr_test.py WC2015.csv

#To run on EMR:
#python emr_test.py -r emr --conf-path mrjob.conf s3://hamlin-mids-assignment4/input/WC2015.csv

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 19:03:10 2015

@author: nicholashamlin
"""

import re

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, JSONValueProtocol
#import sklearn

class MRUniqueTweetCount(MRJob):

    INPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, _, tweet):
        yield tweet['id_str'], 1

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRUniqueTweetCount.run()

#To run locally:
#Simple version: ./emr_test.py WC2015.csv

#To run on EMR:
#python emr_test.py -r emr --conf-path mrjob.conf s3://hamlin-mids-assignment4/input/WC2015.csv

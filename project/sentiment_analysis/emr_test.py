#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 19:03:10 2015

@author: nicholashamlin
"""

import re

from mrjob.job import MRJob
import sklearn

data=[1,2,3,3,3,4,4,4,3,4,5,2,1,5]

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        for i in data:
            yield i, 1

    def reducer(self, key, values):
        total=sum(values)
        yield key, total

if __name__ == '__main__':
    MRWordFrequencyCount.run()

#To run locally:
#Simple version: ./emr_test.py test.csv

#To run on EMR:
#python emr_test.py -r emr --conf-path mrjob.conf s3://hamlin-mids-assignment4/input/WC2015.csv

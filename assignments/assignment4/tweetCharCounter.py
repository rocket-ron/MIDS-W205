#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mrjob.job import MRJob
from mrjob.step import MRStep

class MRTweetCharCount(MRJob):

	def mapper(self, _, line):
		tweet = line.split("|")[4]
		yield 'lines', 1
		yield 'characters', len(tweet)


    # Accumulate the key, values 
	def reducer_(self, key, counts):
		yield key, sum(counts)

if __name__ == '__main__':
	MRTweetCharCount.run()
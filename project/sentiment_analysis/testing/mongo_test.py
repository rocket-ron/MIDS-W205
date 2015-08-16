#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from pymongo_hadoop import BSONMapper
from pymongo_hadoop import BSONReducer

from mrjob.job import MRJob


def bsonmapper(documents):
	while True:
		docs = iter(documents)
		doc = docs.next()
		if not doc:
			break
		yield {'_id' : doc['id']['user.id']}, {'count' : 1}

def bsonreducer(key, values):
	count = 0
	for v in values:
		count += v['count']
	return {'_id' : key, 'count' : count}


class MRWordFrequencyCount(MRJob):

	def mapper(self, _, documents):
		BSONMapper(bsonmapper)

	def reducer(self, key, values):
		BSONReducer(bsonreducer)

if __name__ == '__main__':
	MRWordFrequencyCount.run()



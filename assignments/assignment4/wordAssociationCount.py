#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from mrjob.job import MRJob
from mrjob.step import MRStep

class MRWordAssociationCount(MRJob):

	'''
	# extract the tweet from the CSV file in the 5th field
	# remove any URLs, followed by any non alphanumeric characters
	# for each word in the tweet, yield every other word as a tuple (key) with value 1
	#
	# This regular expression to match URLs is from http://daringfireball.net/2010/07/improved_regex_for_matching_urls
	# and is public domain as licensed by the author.
	'''

	SORT_VALUES = True

	def mapper(self, _, line):
		url_re = re.compile(r"""
			(?xi)
			\b
			(											# Capture 1: entire matched URL
				(?:
					https?://							# http or https protocol
					|									#   or
					www\d{0,3}[.]						# "www.", "www1.", "www2." … "www999."
					|									#   or
					[a-z0-9.\-]+[.][a-z]{2,4}/			# looks like domain name followed by a slash
				)
				(?:										# One or more:
					[^\s()<>]+							# Run of non-space, non-()<>
					|									#   or
					\(([^\s()<>]+|(\([^\s()<>]+\)))*\)	# balanced parens, up to 2 levels
				)+
				(?:										# End with:
					\(([^\s()<>]+|(\([^\s()<>]+\)))*\)	# balanced parens, up to 2 levels
					|									#   or
					[^\s`!()\[\]{};:'".,<>?«»“”‘’]		# not a space or one of these punct chars
				)
			)
			""", re.VERBOSE)
		word_re = re.compile(r"[\w]+")

		# extract the tweet text from the CSV
		tweet = line.split("|")[4]
		# remove URLs from the tweet text
		tweet = url_re.sub('', tweet)
		#
		words = word_re.findall(tweet)

		for word1 in words:
			for word2 in words:
				if word1 == word2:
					continue
				else:
					yield (word1, word2), 1


    # Accumulate the key, values 
	def reducer(self, key, counts):
		yield key, sum(counts)


if __name__ == '__main__':
	MRWordAssociationCount.run()


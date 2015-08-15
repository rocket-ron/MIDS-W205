#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from mrjob.job import MRJob

class MRUrlFrequencyCount(MRJob):

	'''
	# extract the tweet from the CSV file in the 5th field
	# split the tweet into individual terms
	# check if the term matches a URL pattern and if so, yield it as the key with a value 1
	#
	# This regular expression to match URLs is from http://daringfireball.net/2010/07/improved_regex_for_matching_urls
	# and is public domain as licensed by the author.
	'''
	def mapper(self, _, line):
		url = re.compile(r"""
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

		tweet = line.split("|")[4]
		terms = tweet.split()
		for term in terms:
			p = url.search(term)
			if p:
				yield p.group(1), 1

    # Accumulate the key, values 
	def reducer(self, key, values):
		total=sum(values)
		yield key, total

if __name__ == '__main__':
	MRUrlFrequencyCount.run()


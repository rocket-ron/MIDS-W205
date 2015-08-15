#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from sets import Set
from mrjob.job import MRJob

class MRHashtagCount(MRJob):

	'''
	# extract the tweet from the CSV file in the 5th field
	# remove any URLs, and get a list of the three letter hashtags in the tweet
	# for 3 letter hashtag in the tweet, yield key with value 1
	#
	# This regular expression to match URLs is from http://daringfireball.net/2010/07/improved_regex_for_matching_urls
	# and is public domain as licensed by the author.
	'''
	def mapper(self, _, line):
		tags = ('#USA', '#CAN', '#MEX', '#CRC', '#COL', '#ECU', '#BRA', '#NGA', '#CMR',
				'#CIV', '#GER', '#ESP', '#ENG', '#FRA', '#SUI', '#NED', '#SWE', '#NOR',
				'#JPN', '#KOR', '#CHN', '#THA', '#AUS', '#NZL')

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

		hashtag_re = re.compile(r'(\#\b\w{3}\b)')

		tweet = line.split("|")[4]
		tweet = url_re.sub('', tweet)
		hashtags = hashtag_re.findall(tweet)
		for tag in hashtags:
			if tag.upper() in tags:
				yield tag.upper(), 1

    # Accumulate the key, values 
	def reducer(self, key, values):
		total=sum(values)
		yield key, total

if __name__ == '__main__':
	MRHashtagCount.run()


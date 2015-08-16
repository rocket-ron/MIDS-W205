from boto.s3.connection import S3Connection
from boto.s3.key import Key

from pymongo import MongoClient

import StringIO
import json

mongoClient = MongoClient('ec2-54-153-43-230.us-west-1.compute.amazonaws.com')
db = mongoClient.twitter_db

conn = S3Connection(host="s3-us-west-1.amazonaws.com")
bucket = conn.get_bucket('w205-project-twitter-streams')

topics = [ 'ebola','TDF2015', 'trump', 'greece', 'immigration', 'isis']

for topic in topics:
	topic_total = 0
	for key in bucket.get_all_keys(prefix=topic):
		if ('.json' in key.name):
			docs = 0
			chunk = json.loads(key.get_contents_as_string())
			for tweet in chunk:
				if 'lang' in tweet:
					if tweet['lang'] == 'en':
						l = 0L
						try:
							l = long(tweet['id_str'])
						except KeyError:
							pass
						try:
							l = long(tweet['id'])
						except KeyError:
							continue

						if db[topic].find({ "id" : l }).count() == 0:
							db[topic].insert_one(tweet)
							docs += 1
		print 'Inserted {0} docs into {1}'.format(docs, topic)
		topic_total += docs
	print 'Inserted total {0} docs into {1}'.format(topic_total, topic)

mongoClient.close()


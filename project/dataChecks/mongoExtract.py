
from pymongo import MongoClient
from bson.json_util import dumps
import sys

mongoClient = MongoClient('ec2-54-153-43-230.us-west-1.compute.amazonaws.com')
db = mongoClient.twitter_db

topics =['ebola','isis','greece','trump','immigration']

for topic in topics:
	i = 0
	print 'Extracting topic {0}            '.format(topic)
	fname = topic + '.json'
	with open(fname,'w') as f:
		documents = db[topic].find({"lang" : "en"})
		numDocs = documents.count()
		for doc in documents:
			f.write(dumps(doc))
			f.write('\n')
			i += 1
			if i % 1000 == 0:
				sys.stdout.write("Extacted %.2f%%    documents   \r" % (100.0*float(i)/float(numDocs)))
				sys.stdout.flush()

mongoClient.close()

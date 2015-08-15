from pymongo import MongoClient
from bson.json_util import dumps

mongoClient = MongoClient('ec2-54-153-43-230.us-west-1.compute.amazonaws.com')
db = mongoClient.twitter_db

i = 0
with open('ebola.json','w') as isis:
	documents = db['ebola'].find()
	for doc in documents:
		isis.write(dumps(doc))
		i += 1
		if i % 1000 == 0:
			print '{0} docs written...'.format(i)

mongoClient.close()

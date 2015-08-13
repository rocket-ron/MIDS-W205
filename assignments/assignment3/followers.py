from pymongo import MongoClient
import followerFetcher
import sys

# Connect to MongoDB
mongoClient = MongoClient('192.168.194.171', port=27017)
db = mongoClient.db_restT

# create an instance of the FollowerFetcher using the W205-A3F twitter keyset
fetcher = followerFetcher.FollowerFetcher('W205_A3F')

# if an argument is available on the command line, assume it is a single user id
# otherwise query the user id's from the mongoDB retweeters collection
if (len(sys.argv) > 1):
	fetcher.retrieve(sys.argv[1])
else:
	for ids in db.retweets.aggregate( [ { "$group" : { "_id" : "$userid"} } ] ):
		fetcher.retrieve(ids['_id'])


mongoClient.close()
from pymongo import MongoClient
import timelineFetcher

fetcher = timelineFetcher.TimelineFetcher()

mongoClient = MongoClient('192.168.194.171', port=27017)
db = mongoClient.db_restT

users = db.restT.distinct( "user.id_str", { "lang": "en" } )

for user in users:
	print user
	fetcher.retrieve(user)

mongoClient.close()

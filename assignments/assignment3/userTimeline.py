from pymongo import MongoClient
import timelineFetcher

fetcher = timelineFetcher.TimelineFetcher()

mongoClient = MongoClient('192.168.194.171', port=27017)
db = mongoClient.db_restT

# this one is for _all_ the users in the tweets
# users = db.restT.distinct( "user.id_str", { "lang": "en" } )

# this one is for the Top 30 Retweets users
users = db.retweets.distinct( "userid" )

for user in users:
	print user
	fetcher.retrieve(user)

mongoClient.close()

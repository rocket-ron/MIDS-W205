# From the tweets collected, extract the retweets,
# find the top 30 retweets, their author's names,
# and the location of the author if available

from pymongo import MongoClient

# Connect to MongoDB
mongoClient = MongoClient('192.168.194.171', port=27017)
db = mongoClient.db_restT

# assume the following indexes exist (created from MongoDB shell)
# db.restT.createIndex( { "lang" : 1})
# db.restT.createIndex( { "name.id_str" : 1})

# use the MongoDB aggregation pipeline to do the following:
# 1. Filter the retweets using by matching for english retweets
# 2. Group the tweets that have retweets in english by
#	 A. The re-tweeted tweet's id
#	 B. The re-tweeted tweet's author id
#	 C. The re-tweeted tweet's author name
#	 D. The re-tweeted tweet's author location
#	 E. The re-tweeted tweet's text
#	 F. The count of each of occurence
# 3. Sort in descending order
# 4. Limit to the top 30
# 5. Store in the collection called "retweets"
docs = db.restT.aggregate( 
    [
        { "$match" : { "retweeted_status.lang" : "en"}},
        { "$group" : { "_id" : "$retweeted_status.id_str",
                       "userid" : {"$first" : "$retweeted_status.user.id_str"},
                       "name": { "$first" : "$retweeted_status.user.name"},
                       "screen_name" : {"$first" : "$retweeted_status.user.screen_name"},
                       "location" : { "$first" : "retweeted_status.user.location"},
                       "text" : { "$first" : "retweeted_status.text"},
                       "count" : {"$sum" : 1}}},
        { "$sort" :  { "count" : -1}},
        { "$project" : { "count" : 1,
                         "_id" : 1,
                         "name" : 1,
                         "screen_name" : 1,
                         "userid" : 1}},
        { "$limit" : 30},
        { "$out" : "retweets"}
    ])


mongoClient.close()




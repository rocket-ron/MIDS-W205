# From the tweets collected, extract the retweets,
# find the top 30 retweets, their author's names,
# and the location of the author if available

# output to the indicated CSV file

from csv import DictWriter
from pymongo import MongoClient

# Connect to MongoDB
mongoClient = MongoClient('192.168.194.171', port=27017)
db = mongoClient.db_restT

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
docs = db.restT.aggregate( 
    [
        { "$match" : { "retweeted_status.lang" : "en"}},
        { "$group" : { "_id" : {"userid" : "$retweeted_status.id_str",
        						"tweetid" : "$retweeted_status.user.id_str", 
                                "username" : "$retweeted_status.user.name", 
                                "loc" : "$retweeted_status.user.location",
                                "text" : "$retweeted_status.text"},
                       "totRetweets" : {"$sum" : 1 }}},
        { "$sort" : {"totRetweets" : -1}},
        { "$limit" : 30}
    ])

#
#with open('retweeters.csv', 'w') as csvfile:
#    writer = DictWriter(csvfile, fieldnames=['author_id','tweet_id','author_name','author_loc','text','totRetweets'])
#    writer.writeheader()
#    for doc in docs:
#        writer.writerow(doc)
#
#close(csvfile)

for doc in docs:
    print doc

mongoClient.close()




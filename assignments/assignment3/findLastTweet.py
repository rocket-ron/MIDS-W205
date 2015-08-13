from pymongo import MongoClient
import sys
import datetime
from dateutil import parser
import StringIO
import json

# Fri Jul 03 00:00:02 +0000 2015
xsdDatetimeFormat = "%a %b %d %H:%M:%S %z %Y"

# Connect to MongoDB
mongoClient = MongoClient('192.168.194.171', port=27017)
db = mongoClient.db_restT

dates = []
for tweet in db.restT.find({}):
    dates.append(parser.parse(tweet['created_at']))

dates = sorted(dates)

print "First date - " + str(dates[0])
print "Last date  - " + str(dates[-1])

mongoClient.close()




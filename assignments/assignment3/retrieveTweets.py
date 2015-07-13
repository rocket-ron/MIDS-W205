from boto.s3.connection import S3Connection
from boto.s3.key import Key

from pymongo import MongoClient

import StringIO
import json

# Connect to MongoDB
mongoClient = MongoClient('192.168.194.171', port=27017)
db = mongoClient.db_restT

conn = S3Connection(host="s3-us-west-1.amazonaws.com")
bucket = conn.get_bucket('w205-assignment2-rc-data')

# iterate through all the .json files
for k in bucket.get_all_keys(prefix='NBAFinals2015'):
    if ('.json' in k.name):
        # take the chunked tweets and put each JSON in a list element
        chunk = json.loads(k.get_contents_as_string())
        # insert the entire chunk at once
        db.restT.insert_many(chunk)

for k in bucket.get_all_keys(prefix='Warriors'):
    if ('.json' in k.name):
        # take the chunked tweets and put each JSON in a list element
        chunk = json.loads(k.get_contents_as_string())
        # insert the entire chunk at once
        db.restT.insert_many(chunk)

for k in bucket.get_all_keys(prefix='WarriorsAndNBAFinals2015'):
    if ('.json' in k.name):
        # take the chunked tweets and put each JSON in a list element
        chunk = json.loads(k.get_contents_as_string())
        # insert the entire chunk at once
        db.restT.insert_many(chunk)

mongoClient.close()
conn.close()




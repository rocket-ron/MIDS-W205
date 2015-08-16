from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.key import Key
import StringIO
import time
import json

conn = S3Connection(host="s3-us-west-1.amazonaws.com")
bucket = conn.get_bucket('W205-Assignment2-RC-0000'.lower())

s3files = {}
tweetDates = {}
for key in bucket.list():
    s3files[key.name] = time.strptime(key.last_modified, u'%Y-%m-%dT%H:%M:%S.000Z')
    chunk = json.loads(key.get_contents_as_string())
    for tweet in chunk:
        tweetDates[time.strptime(tweet[u'created_at'], u'%a %b %d %H:%M:%S +0000 %Y')] = key.name

f = open('files.txt','w')
for date in sorted(tweetDates):
    f.write(time.strftime(u'%a %b %d %H:%M:%S', date) + '\n')

f.close()

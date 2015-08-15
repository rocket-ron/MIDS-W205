from boto.s3.connection import S3Connection
from boto.s3.key import Key
import StringIO

from whoosh.index import create_in
from whoosh.fields import *
schema = Schema(content=TEXT(stored=True), 
				tweetid=ID(stored=True), 
				user=TEXT(stored=True), 
				userid=ID(stored=True), 
				date=DATETIME(stored=True))



conn = S3Connection(host="s3-us-west-1.amazonaws.com")
bucket = conn.get_bucket('w205-rcordell-assignment4')
key = bucket.get_key('WC2015.csv')
contents = StringIO.StringIO(key.get_contents_as_string())

ix = create_in("indexdir", schema)
writer = ix.writer()

while True:
	line = contents.readline()
	if not line:
		break
	fields = line.split("|")
	writer.add_document(content=fields[4], tweetid=fields[0], userid=fields[1], user=fields[3], date=int(fields[5])*1000*1000)


	        tweet=line.split(",")[1].lower()
        tweet=re.sub(r'[^a-z 0-9]','', tweet)
        words=tweet.split()

writer.commit()

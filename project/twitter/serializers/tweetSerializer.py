import datetime
import time
import json
import uuid
import StringIO
from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.key import Key 


# tweet serializer class from the activities document
class S3ChunkedTweetSerializer(ChunkedTweetSerializer):

	conn = None
	bucket = None

	def __init__(self, tweetsPerChunk, s3BucketName):
		ChunkedTweetSerializer.__init__(self, tweetsPerChunk)
		self.initPersistance(s3BucketName)


	def start(self):
		self._count += 1
		self.out = StringIO.StringIO()
		self.out.write("[\n")
		self._tweetsInFileCount = 0
		self.first = True

	def end(self):
		if self.out is not None:
			self.out.write("\n]\n")
			ts = time.time()
			timeString = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
			key = Key(self.bucket)
			key.key = str(uuid.uuid4()) + "-" + timeString + '.json'
			key.set_contents_from_string(self.out.getvalue())
			self.out.close()
		self.out = None

	def write(self, tweet):
		if self.out is None:
			# take care of the case when we called self.end() to roll to the next file
			self.start()
		if not self.first:
			self.out.write(",\n")
		self.first = False
		self.out.write(json.dumps(tweet._json).encode('utf8'))
		self._tweetsInFileCount += 1
		
		# check to see if we need to roll the file
		if (self._tweetsInFileCount == self._tweetsPerFile):
			self.end()

	def initPersistance(self, bucketName):
		if bucketName is not None:
			self.conn = S3Connection(host="s3-us-west-1.amazonaws.com")
			check = self.conn.lookup(bucketName.lower())
			if check is None:
				self.bucket = self.conn.create_bucket(self._s3BucketName.lower(), location=Location.USWest)
			else:
				self.bucket = self.conn.get_bucket(self._s3BucketName.lower())

	def PersistChunk(self):
		return 0
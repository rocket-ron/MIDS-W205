from chunkedTweetSerializer import ChunkedTweetSerializer
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

	def end(self):
		ChunkedTweetSerializer.end(self, self.persistChunk)

	def initPersistance(self, bucketName):
		if bucketName is not None:
			self.conn = S3Connection(host="s3-us-west-1.amazonaws.com")
			check = self.conn.lookup(str(bucketName).lower())
			if check is None:
				self.bucket = self.conn.create_bucket(str(bucketName).lower(), location=Location.USWest)
			else:
				self.bucket = self.conn.get_bucket(str(bucketName).lower())

	def persistChunk(self):		
			key = Key(self.bucket)
			key.key = ChunkedTweetSerializer.nameChunk(self)
			key.set_contents_from_string(self.out.getvalue())


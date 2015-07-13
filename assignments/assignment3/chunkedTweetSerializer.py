import datetime
import time
import json
import uuid
import StringIO


# tweet serializer class from the activities document
class ChunkedTweetSerializer:
	out = None
	first = True


	def __init__(self, tweetsPerChunk):
		self._tweetsPerChunk = tweetsPerChunk
		self._tweetsInChunkCount = 0
		self._count = 0


	def start(self):
		self._count += 1
		self.out = StringIO.StringIO()
		self.out.write("[\n")
		self._tweetsInChunkCount = 0
		self.first = True

	def end(self, persister):
		if self.out is not None:
			self.out.write("\n]\n")
			persister()
			self.out.close()
		self.out = None

	def write(self, tweet):
		if self.out is None:
			self.start()
		if not self.first:
			self.out.write(",\n")
		self.first = False
		self.out.write(json.dumps(tweet._json).encode('utf8'))
		self._tweetsInChunkCount += 1
		
		# check to see if we need to roll the chunk
		if (self._tweetsInChunkCount == self._tweetsPerChunk):
			self.end()

	# write chunk to file-like object and close the object
	def persistChunk(self, f):
		f.write()
		f.close()

	def nameChunk(self):
		ts = time.time()
		timeString = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
		return str(uuid.uuid4()) + "-" + timeString + '.json'


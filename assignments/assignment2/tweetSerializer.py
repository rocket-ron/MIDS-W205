import json


# tweet serializer class from the activities document
class TweetSerializer:
	out = None
	first = True

	def __init__(self, tweetsPerFile):
		self._tweetsPerFile = tweetsPerFile
		self._tweetsInFileCount = 0
		self._count = 0

	def start(self):
		self._count += 1
		fname = "tweets-"+str(self._count)+".json"
		self.out = open(fname, "w")
		self.out.write("[\n")
		self._tweetsInFileCount = 0
		self.first = True

	def end(self):
		if self.out is not None:
			self.out.write("\n]\n")
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

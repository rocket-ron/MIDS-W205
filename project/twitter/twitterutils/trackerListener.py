from tweepy.streaming import StreamListener
from tweepy import Stream
import twitterAuth
import json
import time
import signal
import threading


class TrackerListener(StreamListener):

	def __init__(self, serializer, key):
		signal.signal(signal.SIGINT, self.interrupt)
		self._lock = threading.RLock()

		self.serializer = serializer
		self.auth = twitterAuth.getOAuth(key)
		self.retryCount = 0
		self.retryTime  = 1
		self.retryMax	= 5
		self.caughtInterrupt = False

	def on_data(self, data):
		# process data
		with self._lock:
			if not self.caughtInterrupt:
				tweet = json.loads(data)
				self.serializer.write(tweet)
				return True
			else:
				self.serializer.end()
				return False


	def on_error(self, status):
		if status_code == 420:
			self.retryCount += 1
			if (self.retryCount > self.retryMax):
				return False
			else:
				time.wait(self.retryTime)
				self.retryTime *= 2
				return True

	def interrupt(self, signum, frame):
		print "CTRL-C caught, closing..."
		with self._lock:
			self.caughtInterrupt = True

	def track(self, track):
		self.twitterStream = Stream(self.auth, self)
		self.twitterStream.filter(track=[track])



	

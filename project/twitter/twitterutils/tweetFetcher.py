import signal
import threading
import tweepy
import twitterAuth

class TweetFetcher:

	def __init__(self, serializer, twitterKey, fetchSize=1500):
		self._serializer = serializer
		self._fetchSize = fetchSize
		auth = twitterAuth.getAppAuth(twitterKey)
            
		self.api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

		signal.signal(signal.SIGINT, self.interrupt)

		# Thanks to Vincent Chio for showing me how to use a mutex in Python
		self._lock = threading.RLock()

	def interrupt(self, signum, frame):
		print(" CTRL-C caught, closing...")
		with self._lock:
			self._serializer.end()
		exit(1)

	def search(self, q):
		try:
			for tweet in tweepy.Cursor(self.api.search,q=q, count=self._fetchSize).items():
				self._serializer.write(tweet._json)
		finally:
			self._serializer.end()

#	thanks to Michael Kennedy for pointing this out to me as an alternative to the Tweepy Cursor
	def search2(self, q):
		last_id = -1
		count = 100
		while True:
			try:
				new_tweets = self.api.search(q=q, count=count, max_id=str(last_id - 1))
				for tweet in new_tweets:
					self._serializer.write(tweet._json)
				last_id = new_tweets[-1].id
			except tweepy.TweepError as e:
				print str(e)
				break
			finally:
				self._serializer.end()



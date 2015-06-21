import signal
import threading
import tweepy
import tweetSerializer

class TweetFetcher:

	def __init__(self):
		# Authentication tokens
		consumer_key = "u15trufXx5JMFi73pGw7W8ijk"
		consumer_secret = "akAIsK6Gd63ViWIDTyLeF8ciOkuT8tQwEQ4xfVFko9JtZ3RaxE"

		access_token = "2030211-EKJ6n9yqbCmlQr0w2BcPZN9XlK72kMFqZRod71bd5L"
		access_token_secret = "fUtvIV5yX37aanszf89vwkEpHGLdU7U3m3ekEstr4cjLl"

#		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
#		auth.set_access_token(access_token, access_token_secret)
		self.api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

		self.serializer = tweetSerializer.TweetSerializer(200, 'W205-Assignment2-RC-both')

		signal.signal(signal.SIGINT, self.interrupt)

		# Thanks to Vincent Chio for showing me how to use a mutex in Python
		self._lock = threading.RLock()

	def interrupt(self, signum, frame):
		print("CTRL-C caught, closing...")
		with self._lock:
			self.serializer.end()
		exit(1)

	def search(self, q):
		self.serializer.start()
		for tweet in tweepy.Cursor(self.api.search,q=q, count=1500).items():
			with self._lock:
				self.serializer.write(tweet)
		self.serializer.end()

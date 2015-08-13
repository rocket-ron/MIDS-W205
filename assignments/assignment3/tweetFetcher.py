import signal
import threading
import tweepy
from mongoTweetSerializer import MongoTweetSerializer
import os

class TweetFetcher:

	def __init__(self):
		# Authentication tokens
		# Authentication tokens from environment variables
		consumer_key = os.getenv('TWITTER_APP_KEY')
		consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')

		access_token = os.getenv('TWITTER_ACCESS_TOKEN')
		access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

#		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
#		auth.set_access_token(access_token, access_token_secret)
		self.api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

		self.serializer = MongoTweetSerializer('db_tweets','lexdiv')

		signal.signal(signal.SIGINT, self.interrupt)

		# Thanks to Vincent Chio for showing me how to use a mutex in Python
		self._lock = threading.RLock()

	def interrupt(self, signum, frame):
		print("CTRL-C caught, closing...")
		with self._lock:
			self.serializer.end()
		exit(1)

	def search(self, q):
		for tweet in tweepy.Cursor(self.api.search,q=q, count=1500).items():
			with self._lock:
				self.serializer.write(tweet)
		self.serializer.end()

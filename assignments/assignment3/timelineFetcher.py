import signal
import threading
import tweepy
from mongoTweetAnalyzer import MongoTweetAnalyzer
import os
import re

class TimelineFetcher:

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

		self.analyzer = MongoTweetAnalyzer('db_restT','lexdiv')

		signal.signal(signal.SIGINT, self.interrupt)

		# Thanks to Vincent Chio for showing me how to use a mutex in Python
		self._lock = threading.RLock()

		self._text = None

	def interrupt(self, signum, frame):
		print("CTRL-C caught, closing...")
		with self._lock:
			self.analyzer.end()
		exit(1)

	def retrieve(self, userId):
		self._text = None
		try:
			for status in tweepy.Cursor(self.api.user_timeline, id=userId, count=3500).items():
				with self._lock:
					self.accumulate(status.text)
			self.analyzer.analyze(self._text, userId)
		except tweepy.TweepError as te:
			if te.reason.lower().find("not authorized"):
				print "User not authorized, skipping..."
			return 0

	def end(self):
		return 0

	def accumulate(self, text):
		t = re.sub(r'^https?:\/\/.*[\r\n]*', '', text)
		if not self._text:
			self._text = t
		else:
			self._text += t


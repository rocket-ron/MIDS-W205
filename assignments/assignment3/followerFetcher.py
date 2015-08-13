import signal
import threading
import tweepy
from mongoFollowerSerializer2 import MongoFollowerSerializer
import twitterAuth
import os
import re
import time

class FollowerFetcher:

	def __init__(self, app):
		auth = twitterAuth.getAppAuth(app)

		self.api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

		self.serializer = MongoFollowerSerializer('db_followers','followers')

		signal.signal(signal.SIGINT, self.interrupt)

		# Thanks to Vincent Chio for showing me how to use a mutex in Python
		self._lock = threading.RLock()

	def interrupt(self, signum, frame):
		print("CTRL-C caught, closing...")
		with self._lock:
			self.serializer.end()
		exit(1)

	def retrieve(self, userId):
		print "Retrieving followers for user id: " + userId
		try:
			for page in tweepy.Cursor(self.api.followers, user_id=userId).pages():	
				with self._lock:
					self.serializer.write(page, userId)
		except tweepy.TweepError as te:
			if te.reason.lower().find("not authorized"):
				print "User not authorized, skipping..."
			return 0


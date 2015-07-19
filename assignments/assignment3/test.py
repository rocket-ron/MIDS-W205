import os
import tweepy

class MyClass:
	@staticmethod
	def write():
		return tweepy.AppAuthHandler(os.getenv('TWITTER_APP_KEY'), os.getenv('TWITTER_CONSUMER_SECRET'))
	@staticmethod
	def getAuth():
		return 0
#		return tweepy.AppAuthHandler(os.getenv('TWITTER_APP_KEY'), os.getenv('TWITTER_CONSUMER_SECRET'))
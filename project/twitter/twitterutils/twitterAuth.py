# Twitter Auth utilities

import tweepy
import os


def getAppAuth(app):
	keys = getKeys(app)
	if len(keys) < 4:
		print "Error retrieving Twitter keys for authorization..."
		return None
	else:
		return tweepy.AppAuthHandler(keys['app_key'], keys['app_secret'])


def getOAuth(app):
	keys = getKeys(app)
	auth = tweepy.OAuthHandler(keys['app_key'], keys['app_secret'])
	auth.set_access_token(keys['access_token'], keys['token_secret'])
	return auth

# keys are environment variables with the patterns
# TWITTER_[app]_APP_KEY
# TWITTER_[app]_CONSUMER_SECRET
# etc

def getKeys(app):
	if app:
		app += '_'
	else:
		app = ''

	keys = {}
	keys['app_key'] = os.getenv('TWITTER_' + app + 'APP_KEY')
	keys['app_secret'] = os.getenv('TWITTER_' + app + 'CONSUMER_SECRET')
	keys['access_token'] = os.getenv('TWITTER_' + app + 'ACCESS_TOKEN')
	keys['token_secret'] = os.getenv('TWITTER_' + app + 'ACCESS_TOKEN_SECRET')
	return keys
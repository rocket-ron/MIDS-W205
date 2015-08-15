import signal
import threading
import requests
from bs4 import BeautifulSoup

class TweetScraper:

	def __init__(self, serializer):

		self._serializer = serializer
		self._retrycount = 0
		self._continue = True

		signal.signal(signal.SIGINT, self.interrupt)

		# Thanks to Vincent Chio for showing me how to use a mutex in Python
		self._lock = threading.RLock()

	def interrupt(self, signum, frame):
		print("CTRL-C caught, closing...")
		with self._lock:
			self.serializer.end()
		exit(1)

	def search(self, q, minTweet, maxTweet):
		self._query = q
		self._maxTweet = maxTweet
		self._minTweet = minTweet
		self.serializer.start()
		continueScraping = True

		while self._continue:
			with self._lock:
				self.serializer.write(scrapeNextPage(q))
		self.serializer.end()
		return (self._minTweet, self._maxTweet)

	def scrapeNextPage(self, query):
		if self._maxTweet:
			position = 'TWEET-{0}-{1}'.format(self._maxTweet,self._minTweet)
			payload = { 'q' : query,
			            'f':'tweets',
			            'src':'typd',
			            'lang':'en',
			            'max_position' : position
			        }
		else:
			payload = { 'q' : query,
			            'f':'tweets',
			            'src':'typd',
			            'lang':'en'
			        }
		
		try:
			r = requests.get(url, payload)
			tweetdata = r.json()
			tweetSoup = BeautifulSoup(tweetdata['items_html'], 'html.parser')
			return extractTweets(tweetSoup.find_all("li", attrs = {"data-item-type":"tweet"}))

		except ConnectionError:
			print "Connection interrupted. Retrying in {0} seconds".format(self._retrycount*30 + 10)
			time.sleep(self._retrycount*30 + 10)
			self._retrycount += 1
			if self._retrycount > 3:
				self._continue = False
		except HTTPError as e:
			print "HTTP error {0}  : {1}".format(e.errno, e.strerror)
			self._continue = False

	def extractTweets(self, listItems):
		tweets = []
		for item in listItems:
			try:
			    tweet = {}
			    if not self._minTweet:
			        self._minTweet = item['data-item-id']
			    self._maxTweet = item['data-item-id']
			    tweet['tweet_id'] = item['data-item-id']
			    tweet['user_id'] = item.div['data-user-id']
			    try:
			    	tweet['user_name'] = item.div['data-name'].encode('ascii','ignore')
			    except KeyError:
			    	tweet['user_name'] = ' '
			    try:
			    	tweet['screen_name'] = item.div['data-screen-name'].encode('ascii','ignore')
			    except KeyError:
			    	tweet['screen_name'] = ' '
			    tweet['text'] = item.find("div", attrs = {"class":"content"}).p.text.encode('ascii','ignore')
			    tweet['time'] = item.find("div", attrs = {"class":"stream-item-header"}).find("a", attrs={"class":"tweet-timestamp js-permalink js-nav js-tooltip"}).span['data-time']
			    tweets.append(tweet)
			except KeyError:
				pass  # skip and move on

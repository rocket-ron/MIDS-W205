import requests
from bs4 import BeautifulSoup
import time
import csv

query = '#FIFAWWC AND (#USA OR #CAN OR #MEX OR #CRC OR #COL OR #ECU OR #BRA OR #NGA OR #CMR OR ' \
		'#CIV OR #GER OR #ESP OR #ENG OR #FRA OR #SUI OR #NED OR #SWE OR #NOR OR #JPN OR #KOR OR ' \
		'#CHN OR #THA OR #AUS OR #NZL) lang:en since:2015-06-05 until:2015-07-06'

url = 'https://twitter.com/i/search/timeline'

payload = { 'q' : query,
	        'f':'tweets',
	        'src':'typd',
	        'lang':'en'
    }

r = requests.get(url, payload)

tweetdata = r.json()
tweetSoup = BeautifulSoup(tweetdata['items_html'], 'html.parser')

first_tweet = None
last_tweet = ''
fieldnames = ['tweet_id', 'user_id', 'user_name','screen_name','text','time']

with open('WC2015.csv','w') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = '|')
	writer.writeheader()

	for item in tweetSoup.find_all("li", attrs = {"data-item-type":"tweet"}):
		try:
		    tweet = {}
		    if not first_tweet:
		        first_tweet = item['data-item-id']
		    last_tweet = item['data-item-id']
		    tweet['tweet_id'] = item['data-item-id']
		    tweet['user_id'] = item.div['data-user-id']
		    tweet['user_name'] = item.div['data-name'].encode('ascii','ignore')
		    tweet['screen_name'] = item.div['data-screen-name'].encode('ascii','ignore')
		    tweet['text'] = item.find("div", attrs = {"class":"content"}).p.text.encode('ascii','ignore')
		    tweet['time'] = item.find("div", attrs = {"class":"stream-item-header"}).find("a", attrs={"class":"tweet-timestamp js-permalink js-nav js-tooltip"}).span['data-time']
		    writer.writerow(tweet)
		except:
			pass # if we get an error, skip this one and move on

	page = 1
	while True:
		position = 'TWEET-{0}-{1}'.format(last_tweet,first_tweet)
		payload = { 'q' : query,
		            'f':'tweets',
		            'src':'typd',
		            'lang':'en',
		            'max_position' : position
		        }
		r = requests.get(url, payload)
		if r.status_code == requests.codes.ok:
			tweetdata = r.json()

			tweetSoup = BeautifulSoup(tweetdata['items_html'], 'html.parser')

			for item in tweetSoup.find_all("li", attrs = {"data-item-type":"tweet"}):
				try:
				    tweet = {}
				    if not first_tweet:
				        first_tweet = item['data-item-id']
				    last_tweet = item['data-item-id']
				    tweet['tweet_id'] = item['data-item-id']
				    tweet['user_id'] = item.div['data-user-id']
				    tweet['user_name'] = item.div['data-name'].encode('ascii','ignore')
				    tweet['screen_name'] = item.div['data-screen-name'].encode('ascii','ignore')
				    tweet['text'] = item.find("div", attrs = {"class":"content"}).p.text.encode('ascii','ignore')
				    tweet['time'] = item.find("div", attrs = {"class":"stream-item-header"}).find("a", attrs={"class":"tweet-timestamp js-permalink js-nav js-tooltip"}).span['data-time']
				    writer.writerow(tweet)
				except:
					pass  # skip and move on
		else:
			print "Recieved NOT OK status response {0}  ... exiting".format(r.status_code)
			break
		print 'Page {0} processed... last tweet id {1}'.format(page, last_tweet)
		page += 1
		time.sleep(5)

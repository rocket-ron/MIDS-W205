## Scan through a set of .json files in an S3 bucket for tweets and the text therein
## tokenize each tweet, filter for stop words and puncuation and other things
## show a frequency/histogran of the word distribution
import sys
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from nltk import word_tokenize
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

import json

# Connect to the bucket
if (len(sys.argv) < 2):
	sys.exit(2)

conn = S3Connection(host="s3-us-west-1.amazonaws.com")
bucket = conn.get_bucket(sys.argv[1].lower())

stop = stopwords.words('english')
stop.extend(['rt','http','https','co','1','2','3','4','5','6','7','8','9'])
tokenizer = RegexpTokenizer(r'\w+')

words = []
# iterate through all the .json files
for k in bucket.get_all_keys(prefix=sys.argv[2]):
	if ('.json' in k.name):
		chunk = json.loads(k.get_contents_as_string())
		for tweet in chunk:
			if (tweet[u'lang'] == 'en'):
				text = tweet[u'text']
				words.extend([i for i in tokenizer.tokenize(text.lower()) if i not in stop])

conn.close()
# Now we should have a list of all the English words that are not in the stop word list
fdist = FreqDist(words)
fdist.plot(30, cumulative=False)


from pymongo import MongoClient
from nltk import word_tokenize
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re
from collections import Counter

# tweet serializer class from the activities document
class MongoTweetAnalyzer():

	_collection = None
	_client = None

	def __init__(self, database, collection):
		self.initPersistance(database, collection)

	def analyze(self, text, userId):
		corpus = []
		stop = stopwords.words('english')
		stop.extend(['rt','http','https','co','1','2','3','4','5','6','7','8','9'])
		tokenizer = RegexpTokenizer(r'\w+')

		corpus.extend([i for i in tokenizer.tokenize(text.lower()) if i not in stop])

		c = Counter(corpus)

		lexicon = {}
		lexicon['user_id'] = userId
		lexicon['word_count'] = len(corpus)
		lexicon['postings'] = dict(c)
		lexicon['unique_count'] = len(dict(c))
		lexicon['diversity'] = float(lexicon['unique_count'])/float(lexicon['word_count'])

		self.write(lexicon)

	def write(self, lexicon):
		if (self._collection == None):
			initPersistance()
		
		self._collection.insert_one(lexicon)

	def end(self):
		if (self._client != None):
			self._client.close()

	def initPersistance(self, database, collection):
		self._client = MongoClient('192.168.194.171', port=27017)
		self._collection = self._client[str(database)][str(collection)]

from pymongo import MongoClient
import json

# tweet serializer class from the activities document
class MongoTweetSerializer():

	_collection = None
	_client = None

	def __init__(self, host, database, collection):
		self.host = host
		self.database = database
		self.collection = collection
		self.initPersistance(self.host, self.database, self.collection)

	def write(self, tweet):
		if (self._collection == None):
			initPersistance(self.host, self.database, self.collection)

		self._collection.insert_one(tweet)

	def end(self):
		if (self._client != None):
			self._client.close()

	def initPersistance(self, host, database, collection):
		self._client = MongoClient(host=host, port=27017)
		self._collection = self._client[str(database)][str(collection)]

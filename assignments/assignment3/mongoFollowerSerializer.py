from pymongo import MongoClient
import json

# tweet serializer class from the activities document
class MongoFollowerSerializer():

	_collection = None
	_client = None

	def __init__(self, database, collection):
		self.initPersistance(database, collection)

	def write(self, page, userId):
		if (self._collection == None):
			initPersistance()

		for userObj in page:
			self._collection.insert_one({'user'			: userId, 
										'id_str'		: userObj.id_str, 
										'name'			: userObj.name, 
										'screen_name'	: userObj.screen_name})

	def end(self):
		if (self._client != None):
			self._client.close()

	def initPersistance(self, database, collection):
		self._client = MongoClient('192.168.194.171', port=27017)
		self._collection = self._client[str(database)][str(collection)]

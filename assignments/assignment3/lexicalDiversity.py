import matplotlib.pyplot as plt 
import numpy as np
from pymongo import MongoClient
import collections

mongoClient = MongoClient('192.168.194.171', port=27017)
db = mongoClient.db_restT

docs = db.lexdiv2.aggregate( 
    [
        { "$group" : { "_id" : "$user_id",
                       "diversity" : {"$first" : "$diversity"},
                       "followers_count" : { "$first" : "$followers_count"} }},
        { "$sort" :  { "followers_count" : -1}},
        { "$project" : { "diversity" : 1,
        				 "followers_count" : 1,
                         "_id" : 1}}
    ])

max_followers = 0
lex = {}
follower_lex = []
for doc in docs:
	lex[doc['_id']] = doc['diversity']
	if doc['followers_count'] < 2000:
		follower_lex.append((doc['followers_count'], doc['diversity']))
		if doc['followers_count'] > max_followers:
			max_followers = doc['followers_count']


bar = plt.bar(range(len(lex)), lex.values(), align='center')
plt.ylabel('Lexical Diversity')
plt.xlabel('User Sequence Sorted By Number of Followers')
plt.title('Lexical Diversity for Users in order of Follower Count')
plt.setp(bar, color='blue')
plt.axis([0, len(lex), 0.25, 1.0])
plt.show()

plt.scatter(*zip(*follower_lex))
plt.axis([0, max_followers, 0.25, 1.0])
plt.ylabel('Lexical Diversity')
plt.xlabel('Number of Followers')
plt.title('Lexical Diversity by Follower Count')
plt.show()


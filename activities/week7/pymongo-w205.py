
# coding: utf-8

# ### Connecting to MongoDB using Pymango

# In[1]:

import pymongo

try:
    conn=pymongo.MongoClient()
    print "Connected!"
except pymongo.errors.ConnectionFailure, e:
   print "Connection failed : %s" % e 
conn


# In[2]:

test_db = conn['MIDS-w205']
test_db


# In[3]:

conn.database_names()


# 
# 
# ### Collections
# 
# Group of documents stored in MongoDB are called collections

# In[5]:

myColl = test_db.my_collection
myColl


# In[6]:

test_db.collection_names()


# ### Documents
# 

# In[7]:

myDoc = {"name":"Arash","family name":"Nourian","faculty":"I school", "age":"100"}


# In[8]:

myColl.insert(myDoc)


# In[9]:

myColl.insert({"name":"Coye","family name":"Cheshire","faculty":"I school", "age":"110"})


# In[10]:

conn.database_names()


# In[12]:

test_db.collection_names()


# In[14]:

rec=myColl.find_one({"name": "Arash"})
print rec


# In[15]:

print rec['faculty']


# In[16]:

documents = list(myColl.find())
documents


# In[17]:

print myColl.count()


# In[18]:

myColl.distinct("name")


# In[ ]:

myColl.remove({'name': 'Arash'})


# In[22]:

list(myColl.find({'age': {'$gt': '100'}}))


# In[46]:

list(myColl.find({'faculty': 'I school','age': {'$gt': '100'}}))


# In[47]:

list(myColl.find({'faculty': 'I school', 'name': {'$ne': 'Coye'}}))


# In[48]:

list(myColl.find({'name': {'$regex': 'h$'}}))



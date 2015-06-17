
# coding: utf-8

# ## JSON (Javascript Object Notation) is used for data interchange of following DT:
# 
# ###Lists (JSON arrays)
# ###Dicts (JSON objects)
# ###Other types
# 
# #To load a jason file we call json.loads() method that takes a JSON string and returns the corresponding DT.

# In[ ]:

import requests
import json


# In[119]:

response = requests.get("http://api.openweathermap.org/data/2.5/box/city?bbox=12,32,15,37,10&cluster=yes")


# In[ ]:

response.ok


# In[120]:

myData = json.loads(response.content.decode("utf-8"))


type(myData)
len(myData)
myData


# In[118]:

import urllib2

req = urllib2.urlopen('http://api.openweathermap.org/data/2.5/box/city?bbox=12,32,15,37,10&cluster=yes')
myData2 = json.load(req)   
print myData2


# In[ ]:

myData


# In[121]:

lookUp = myData[u'list']
lookUp


# In[122]:

for item in lookUp:
    
    print item.get(u'id')
    


# In[123]:

for item in lookUp:
    print item.get(u'coord').get(u'lat')


# In[ ]:




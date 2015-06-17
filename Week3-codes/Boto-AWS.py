
# coding: utf-8

# ## Accessing AWS using Boto

# In[ ]:

from boto.s3.connection import S3Connection


# In[ ]:

conn = S3Connection('AKIAJFBG7KZDYBFM3HBA', 'iKucsLWltkP0UuYrazaf010bBvgnK2pi5RnEDpRm')


# ## Alternative is  conn = boto.connect_s3()

# In[ ]:

bucket = conn.create_bucket('boto-w2015-2014')


# ##Key object is needed to keep track of data stored in S3. 
# ##To store new data in S3, we need a new Key object:
# 

# In[ ]:

from boto.s3.key import Key

myKey = Key(bucket)
myKey.key = 'mylist.txt'
myKey.set_contents_from_string('Lets write something in this bucket')


# ## Accessing a bucket

# In[ ]:

myBucket = conn.get_bucket('mybuck-w205-2014') 
for key in myBucket.list():
    print key.name.encode('utf-8')


# ##Deleting a bucket

# In[ ]:


for key in myBucket.list():
    key.delete()

conn.delete_bucket('mybuck-w205-2014')


# In[ ]:




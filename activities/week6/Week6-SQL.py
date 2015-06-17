
# coding: utf-8

# In[ ]:


import pandas as pd


# ## Tools and libraries

# ## Creating or using a Database

# In[ ]:

import sqlalchemy


# In[ ]:

myEngine = create_engine('sqlite:///my.db')


# ## `pandas.io.sql`

# In[ ]:

from pandas.io import sql


# In[ ]:

mDf=sql.read_sql_table('tips', myEngine)
mDf.head()


# In[ ]:

mDf.to_sql('tip', myEngine)


# In[ ]:

new_df = sql.read_sql_table('tip', myEngine)


# In[ ]:

new_df.head()


# ##db.py

# In[ ]:

import db


# In[ ]:

mConn = db.DB(filename='Chinook_Sqlite.sqlite', dbtype='sqlite')


# In[ ]:

mConn.tables


# In[ ]:

mConn.tables.Customer


# Using the `.head()` method, you can get back the head of the table. Querry is (`SELECT * FROM Customer LIMIT 6`).

# In[ ]:

mConn.tables.Customer.head()


# In[ ]:

mConn.tables.Customer.sample()


# In[ ]:

mConn.tables


# In[ ]:

mConn.find_column('*Name')


# In[ ]:

mConn.tables.Artist.head()


# In[ ]:

mConn.tables.Album.head()


# In[ ]:

mConn.query("""
SELECT Album.Title FROM Album
    LEFT JOIN Artist
    ON Artist.ArtistId=Album.ArtistId
""")


# In[ ]:




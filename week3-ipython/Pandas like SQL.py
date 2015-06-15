
# coding: utf-8

# # Pandas Cont..

# In[ ]:

from pandas import DataFrame
import pandas as pd



# In[ ]:

df = DataFrame(data = {'Col1':[10,12,13],
                       'Col2':['txt1','txt2','txt3'],
                       'Col3':[10,12,13]})
df


# In[ ]:

df.count()


# # Updating tables

# In[ ]:


# Create where statement

cond = df['Col3'] > 10

# Update corresponding cols with the condition
df['Col1'][cond] = 1
df['Col2'][cond] = 'text1'
df


# # Inserting into a table from another table

# In[ ]:


df2 = df
df


# #Joining two tables

# In[ ]:



# inner join
df.merge(df2,left_on='Col1',right_on='Col1')

# left join
df.merge(df2,left_on='Col1',right_on='Col1',how='left')


# # Selecting known number of rows

# In[ ]:


df.head(2)
df.tail(2)


# # Sorting

# In[ ]:


df.sort(ascending=True,columns=['Col3'])

#descending
df.sort(ascending=False,columns=['Col3'])


# #Finding unique values

# In[ ]:


df['Col1'].unique()


# In[ ]:

df


# # Using Lambda to update records

# In[ ]:


df['Col1'].apply(lambda x: 100 if x==1 else 120 )


# # SQL "IN" equivalent

# In[ ]:


"""
SELECT * FROM t1 WHERE Col1 IN (1,100)
"""


subset = df['Col1'].isin([1])
df[subset]


# # String matching

# In[ ]:



cond = df['Col2'].str.startswith('tx')

df[cond]


# In[ ]:




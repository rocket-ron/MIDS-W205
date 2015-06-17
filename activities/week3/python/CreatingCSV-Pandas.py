
# coding: utf-8

# In[ ]:

import csv

mFile = open('MIDSDS.csv','rb') 

reader =csv.reader(mFile)


# In[ ]:

d = [i for i in  reader] 


print d


# In[ ]:

d=d+[['Mike','32','MIDS15']]
print d


# In[ ]:

d= [[row[0],eval(row[1])+1,row[2]] for row in reader]

print d


# In[ ]:

out=open('MIDS_out.csv','wb')
output=csv.writer(out)

for row in d:
    output.writerow(row)
out.close()


# In[ ]:

mFile = open('MIDS_out.csv','rb') 

reader =csv.reader(mFile)
d = [i for i in  reader] 


print d


# ##Using Pandas for creating CSV file

# In[ ]:

import os
from pandas import DataFrame, read_csv
import pandas as pd 


# In[ ]:




# In[ ]:

names = ['Nick','Joe','Jessy','Ali']
ages = [27, 25, 31, 36, 29]
program =['MIDS13','MIDS14','MIDS14','MIDS13']


# In[ ]:


MIDSDS = zip(names,ages,program)
MIDSDS


# In[ ]:

df = pd.DataFrame(data = MIDSDS, columns=['Name', 'Age','Program'])
df


# In[ ]:

df.to_csv('MIDSDS.csv',index=False,header=False)


# In[ ]:

ds = r'MIDSDS.csv'
df = pd.read_csv(ds,names=['Name', 'Age','Program'])


# In[ ]:

df


# In[ ]:

os.remove(ds)


# ## Two good tools for working with JSON and CSV on the command line:
# ##1-JQ
# ##2-CSVKit

# In[ ]:




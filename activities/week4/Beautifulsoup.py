
# coding: utf-8

# ##Using Beautifulsoup for XML processing

# In[26]:

from bs4 import BeautifulSoup

from urllib import urlopen

html = urlopen("http://www.ischool.berkeley.edu/newsandevents/events/deanslectures").read()
soup = BeautifulSoup(html)

print soup.findAll('div',{"class":"views-field-title"})



# In[27]:



for section in soup.find('div',{"class":"views-field-title"}).a.contents:

    print section


# In[28]:

for section in soup.findAll('div',{"class":"views-row"}):
    
    print section.findChildren()[2].a.contents
    



# In[ ]:

for section in soup.findAll('div',{"class":"views-row"}):
   print section.findChildren()[1].contents


# In[ ]:




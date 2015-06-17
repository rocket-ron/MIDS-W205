
# coding: utf-8

# ## Using Scrapy to crawl the web

# In[ ]:

sudo pip install Scrapy


# In[ ]:

get_ipython().system(u'scrapy startproject iSchoolCrl')


# In[ ]:

get_ipython().system(u'ls ./iSchoolCrl')


# ##Item.py is a container for the crawled data. We modify it by our own class 

# In[ ]:

get_ipython().system(u'cat ./iSchoolCrl/items.py')


# In[ ]:

get_ipython().system(u'cat ./iSchoolCrl/items.py')


# ##Spider is the class that actually does the crawling

# In[ ]:

get_ipython().system(u'ls ./iSchoolCrl/spiders')


# ##Scrapy uses XPath, a language that finds information within HTML/XML
# 
# 

# In[ ]:

html(/body/p:, selects, the, <p>, element, inside, the, <body>, element.)
(/p, selects, ALL, <p>, elements, inside, the, HTML.)
(/p[@class=”Cname”], selects, all, <p>, elements, with, attribute, class=”Cname”, like, <p, class=”Cname”>.)
(/p[contains(@class,, ”Cname”)], selects, all, <p>, elements, with, attribute, “class”, containing, ”Cname”, like, <p, class=”Cname1)
and <p class=”MyCname”>


# In[ ]:

from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from iSchoolCrl.items import iSchoolItem

class MySpider(Spider):
    name = "ischool"
    allowed_domains = ["berkeley.edu"]
    start_urls = ["http://www.ischool.berkeley.edu/people/faculty"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//div[@class='title']")
        items = []
      	for titles in titles:
          	item = iSchoolItem()
          	item ["name"] = titles.select("a/text()").extract()
          	item ["link"] = titles.select("a/@href").extract()
          	items.append(item)
      	return items


# In[ ]:

get_ipython().system(u'scrapy crawl ischool')


# In[ ]:

get_ipython().system(u'scrapy crawl ischool -o items.csv -t csv')


# In[ ]:

from pandas import DataFrame, read_csv
import pandas as pd 

ds = r'items.csv'
df = pd.read_csv(ds,names=['Link', 'Faculy Name'])
df


# ## Crawling in different formats
# ## scrapy crawl ischool -o ischool.json -t json

# In[ ]:




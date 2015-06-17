
# coding: utf-8

## NLTK

# NLTK provides easy-to-use interfaces for text processing including classification, tokenization, stemming, tagging, parsing, and semantic reasoning

# In[74]:

get_ipython().magic(u'matplotlib inline')


# In[2]:

# import the library and download sample texts
import nltk
nltk.download()


# In[2]:

from nltk.book import *


# ## Tokenizing a text

# In[ ]:

myText = ["It is really good", "I do not like it"]


# In[ ]:

import nltk
tokens = [word_tokenize(txt) for txt in myText]
print tokens


# ##Finding part of speach 

# In[ ]:


speechTag=nltk.pos_tag(tokens[0])
speechTag


# ##Chunking and ne_chunk

# In[ ]:

print nltk.ne_chunk(speechTag)


# In[ ]:




# In[3]:

# examine concordances (word + context)
text1.concordance("Whale")


# ##Distributional similarity: words that that occur frequently in the same context and with a similar distribution

# In[76]:

text1.similar("big")


# In[7]:

# see where in a text certain words are found to occur
text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])


# In[75]:

guten = nltk.text.Text(nltk.corpus.gutenberg.words())
guten.dispersion_plot(["sea", "whale", "ship", "crew"])


# In[81]:

# the texts are just lists of strings
text2[:-10]


# In[82]:

# count of all tokens (including punctuation)
len(text2)


# In[84]:

# number of distinct tokens
len(set(text2))


# In[84]:




# In[11]:

# build a frequency distribution
fdist1 = FreqDist(text1) 
fdist1


# In[12]:

fdist1.most_common(20)


# In[13]:

fdist1['whale']


# In[14]:

fdist1.plot(20, cumulative=True)


# In[85]:

# apply a list comprehension to get words over 10 characters
V = set(text1)
long_words = [w for w in V if len(w) > 10]
sorted(long_words)


# In[87]:

# word sequences that appear together unusually often
text4.collocations()


### Raw Text Processing

# In[13]:

# download raw text from an online repository
import urllib2
url = "http://www.gutenberg.org/files/12345/12345.txt"
response = urllib2.urlopen(url)
source = response.read().decode('utf8')
len(source)


# In[14]:

source[:21]


# In[28]:

# tokenize the raw text

import nltk

words = word_tokenize(source)
len(words)


# In[29]:

words[:5]


# In[31]:

text = nltk.Text(words)
text[500:515]


# In[34]:

text.collocations()


# In[38]:

source.find("Barry")


# In[42]:

from bs4 import BeautifulSoup
url = "http://money.cnn.com/2015/06/08/technology/apple-wwdc-2015/index.html"
html = urllib2.urlopen(url).read().decode('utf8')
source = BeautifulSoup(html).get_text()
words = word_tokenize(source)
words[0:20]


# In[43]:

# isolate just the article text
#words = words[110:390]
text = nltk.Text(words)
text.concordance('iPhone')


### Regular Expressions

# In[57]:

# regular expression library
import re
wordlist = [w for w in nltk.corpus.words.words('en') if word.islower()]


# In[59]:

# match the end of a word
[w for w in wordlist if re.search('ing$', w)][0:25]


# In[60]:

# wildcard matches any single character
[w for w in wordlist if re.search('^..j..t..$', w)][0:10]


# In[61]:

# combination of caret (start of word) and sets
[w for w in wordlist if re.search('^[ghi][mno][jlk][def]$', w)]


# In[66]:

# using "findall" to extract partial matches from words
fd = nltk.FreqDist(vs for word in wordlist 
                      for vs in re.findall('[aeiou]{2,}', word))
fd.most_common(10)


### Tagging

# In[91]:

# Use a built-in tokenizer and tagger
text = word_tokenize("They refuse to permit us to obtain the refuse permit")
nltk.pos_tag(text)


# In[92]:

tags = [b for (a, b) in nltk.pos_tag(text)]
fd = nltk.FreqDist(tags)
fd.tabulate()


# In[103]:

nltk.corpus.brown.tagged_words()[0:5]


# In[105]:

# Word similarity using a pre-tagged text
text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())

text.similar('girl')


# In[48]:

from nltk.corpus import brown
brown_news_tagged = brown.tagged_words(categories='news', tagset='universal')
tag_fd = nltk.FreqDist(tag for (word, tag) in brown_news_tagged)
tag_fd.most_common()


# ## Working with sample texts
# 

# In[ ]:

mobyText = nltk.text.Text(nltk.corpus.gutenberg.words('melville-moby_dick.txt'))
mobyText.similar("whale")


### Classifying Text

# NLTK allows you to define your own text classifier (feature sets,...) and perform sentiment analysis
# 


# coding: utf-8

## Whoosh : A fast, featureful full-text indexing and searching library 

# ---

# 
# 
# ![whoosh](http://files.whoosh.ca/whoosh/whoosh_logo.png)
# 
# 
#     
# Install whoosh using pip:
# 
#     pip install whoosh 
#     
# 

# ---

### The Index

# Defining an `Index` schema:
# 
# 1. id 
# 2. author 
# 3. title 
# 4. text 
# 5. path 
# 6. source 
# 
# 

# In[20]:

from whoosh.fields import Schema


# In[20]:




# In[30]:

from whoosh.fields import ID, KEYWORD, TEXT

my_schema = Schema(id = ID(unique=True, stored=True), 
                    path = ID(stored=True), 
                    source = ID(stored=True),
                    author = TEXT(stored=True), 
                    title = TEXT(stored=True),
                    text = TEXT)


# In[30]:




# In[31]:

import os

from whoosh.index import create_in

if not os.path.exists("1-index"):
    os.mkdir("1-index")
    index = create_in("1-index", my_schema)


# 

# In[32]:

from whoosh.index import open_dir

index = open_dir("1-index")


# 

# In[33]:

writer = index.writer()


# 

# In[34]:

import io
writer.add_document(id = u'guten01', 
                    path = u'data/austen-emma.txt',
                    source = u'austen-emma.txt',
                    author = u'Jane Austen',
                    title = u'Emma',
                    text = io.open('data/austen-emma.txt', encoding='utf-8').read())


# 

# In[35]:

writer.add_document(id = u'guten02', 
                    path = u'data/austen-persuasion.txt',
                    source = u'austen-persuasion.txt',
                    author = u'Jane Austen',
                    title = u'Chapter 1',
                    text = io.open('data/austen-persuasion.txt', encoding='utf-8').read())

writer.add_document(id = u'guten03', 
                    path = u'data/blake-poems.txt',
                    source = u'blake-poems.txt',
                    author = u'William Blake',
                    title = u'SONGS OF INNOCENCE AND OF EXPERIENCE and THE BOOK of THEL',
                    text = io.open('data/austen-persuasion.txt', encoding='utf-8').read())



# 

# In[36]:

writer.commit()


# ---

### Querying

# 

# In[37]:

searcher = index.searcher()


# 

# In[38]:

from whoosh.query import Term, And

query = And([Term("text", "song"), Term("text", "wild")])


# 

# In[46]:

results = searcher.search(query)
print('# of hits:', len(results))
print('Best Match:', results[0])


# Whoosh' `QuerParser` object automatically parse strings into `Query` objects

# In[41]:

from whoosh.qparser import QueryParser

parser = QueryParser("text", index.schema)


# 

# In[42]:

parser.parse("song wild person")


# In[43]:

parser.parse("(song OR wild) AND (song OR austen)")


# In[45]:

parser.parse("song wild author:'William Blake'")





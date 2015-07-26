
# coding: utf-8

# ## TF-IDF 

# The tf-idf  of a word, w, is
#       $$tf(w) * idf(w)$$
#       
# Where tf(w) = (Number of times the word appears in a document) / (Total number of words in the document)
# 
# idf(w) = log(Number of documents / Number of documents that contain word w ).

# In[22]:

from math import log

q_terms = ['Berkeley', 'MIDS']

def tf(term, doc):
    doc = doc.lower().split()
    return doc.count(term.lower()) / float(len(doc))
   

def idf(term, corpus):
    num_doc_with_term =  0
    for text in corpus:
     if term.lower() in text.lower().split():
        num_doc_with_term+=1
    return 1.0 + log(float(len(corpus)) / num_doc_with_term)
   

def tf_idf(term, doc, corpus):
    return tf(term, doc) * idf(term, corpus)



corpus =     {'1': 'The School of Information is both UC Berkeley newest and its smallest school.            Located in the center of campus, the I School is a graduate research and education           community committed to expanding access to information and to improving its usability,            reliability, and credibility while preserving security and privacy. ',
     
     '2': 'Based in UC Berkeley  historic South Hall, roughly 150 graduate students and 18 faculty members form \
            a small, multi-disciplinary collective of scholars and practitioners.',
     
     '3': 'The I School at Berkeley offers two professional master’s degrees and an academic doctoral degree. \
           Our MIMS program trains students for careers as information professionals and emphasizes \
           small classes and project-based learning.' ,
     '4': 'The Master of Information and Data Science (MIDS) program at Berkeley is an innovative part-time fully \
           online program that trains data-savvy professionals and managers. Working with data at scale \
           requires distinctive new skills and tools. The MIDS program is distinguished by its disciplinary \
           breadth; unlike other programs that focus on advanced mathematics and modeling alone, \
           the MIDS degree provides students insights from social science and policy research,\
           as well as statistics, computer science and engineering.'}
      
           
q_scores = {'1': 0, '2': 0, '3': 0, '4': 0}
for term in [t.lower() for t in q_terms]:
    for doc in corpus:
        print 'TF(%s): %s' % (doc, term), tf(term, corpus[doc])
    print 'IDF: %s' % (term, ), idf(term, corpus.values())
    print

    for doc in corpus:
        score = tf_idf(term, corpus[doc], corpus.values())
        print 'TF-IDF(%s): %s' % (doc, term), score
        q_scores[doc] += score
    print

print "TF-IDF scores for the query terms'%s' are" % (' '.join(q_terms), )
for (doc, score) in q_scores.items():
    print doc, score


# In[ ]:




# ## PageRank
# 
# PageRank is a algorithm used by Google to rank the 'importance' of a web page. 

# <a><img src= "http://upload.wikimedia.org/wikipedia/commons/6/69/PageRank-hi-res.png"  height=60% width=60%></a>

# In[1]:




# <a><img src= "formula.png"  height=70% width=70%></a>

# In[ ]:




# In[ ]:




# ### Sample Problem
# 

# In[ ]:




# In[31]:

import networkx as nx

# Create a directed networkx graph
linkG = nx.DiGraph()

# Add web pages (graph nodes)
for i in range(5):
   linkG.add_node(i, label="p" + str(i))

# Add outgoing web links with weights (directed graph edges)
linkG.add_edge(0, 1)
linkG.add_edge(0, 2)
linkG.add_edge(0, 3)
linkG.add_edge(0, 4)
linkG.add_edge(1, 2)
linkG.add_edge(1, 3)
linkG.add_edge(1, 4)

linkG.add_edge(2, 0)
linkG.add_edge(2, 1)

linkG.add_edge(3, 0)
linkG.add_edge(3, 2)

linkG.add_edge(4, 1)
linkG.add_edge(4, 2)
linkG.add_edge(4, 3)

G = nx.to_agraph(linkG)
G.layout(prog='dot')
G.draw('test.png')
from IPython.display import Image
Image('test.png')


# 
# 
# If we denote the page rank of page $p_{i}$ by $pr_{i}$, we can express the importance of each page:
# 
# $$
# \begin{align}
# pr_{0} =& \tfrac{1}{2} pr_{2} + \tfrac{1}{2} pr_{3}
# \\
# pr_{1} =& \tfrac{1}{4}pr_{0} + \tfrac{1}{2}pr_{2} + \tfrac{1}{3}pr_{4} 
# \\
# pr_{2} =& \tfrac{1}{4}pr_{0} + \tfrac{1}{3}pr_{1} + \tfrac{1}{2}pr_{3} + \tfrac{1}{3}pr_{4}
# \\
# pr_{3} =& \tfrac{1}{4}pr_{0} + \tfrac{1}{3}pr_{1} + \tfrac{1}{3}pr_{4}
# \\
# pr_{4} =& \tfrac{1}{4}pr_{0} + \tfrac{1}{3}pr_{1}
# \end{align}
# $$
# 
# We can express this as a system of equation:
# 
# $$
# \underbrace{
# \begin{bmatrix}
# 0 & 0 & \tfrac{1}{2} & \tfrac{1}{2} & 0
# \\
# \tfrac{1}{4} & 0 & \tfrac{1}{2} & 0 & \tfrac{1}{3}
# \\
# \tfrac{1}{4} & \tfrac{1}{3} & 0 & \tfrac{1}{2} & \tfrac{1}{3}
# \\
# \tfrac{1}{4} & \tfrac{1}{3} & 0 & 0 & \tfrac{1}{3}
# \\
# \tfrac{1}{4} & \tfrac{1}{3} & 0 & 0 & 0
# \end{bmatrix}}_{\boldsymbol{A}}
# \begin{bmatrix}
# pr_{0} \\ pr_{1} \\ pr_{2} \\ pr_{3} \\ pr_{4}
# \end{bmatrix}
# =
# \begin{bmatrix}
# pr_{0} \\ pr_{1} \\ pr_{2} \\ pr_{3} \\ pr_{4}
# \end{bmatrix}
# $$
# 
# 
# 

# In[4]:

A = (nx.adjacency_matrix(G).T)


# In[ ]:




# First, we will create a link martix for our graph.

# In[23]:

import numpy as np
nodes = 5 
M_link = np.zeros((nodes, nodes)) 

M_link[:,0] = 1 
M_link[2,1] = 1
M_link[3,1] = 1 
M_link[4,1] = 1 


M_link[1,2] = 1 
M_link[0,2] = 1 

M_link[0,3] = 1 
M_link[2,3] = 1 


M_link[1,4] = 1 
M_link[1,4] = 1 
M_link[3,4] = 1

print(M_link)


# Next we need to create the adjacency matrix by dividing each column by its sum:

# In[24]:

M_adj = np.empty((nodes, nodes))
for j in range(nodes):
    M_adj[:,j] = M_link[:,j] / M_link[:,j].sum()
np.set_printoptions(precision=4)
print(M_adj)


# Finally we need to apply the `pagerank` function, which will apply page transitions iteratively to a randomly initialized distribution over the pages, until convergence.

# In[10]:

import numpy as np
def pagerank(M_adj, d=0.85, square_error=1e-5):
    
    nodes = M_adj.shape[0] 
    
    V_pr = np.random.rand(nodes)
    
    v_pr = V_pr / V_pr.sum() 
    last_v = np.ones((nodes)) 
    M_hat = d * M_adj + (1-d)/nodes * np.ones((nodes, nodes)) 
    while np.square( v_pr - last_v).sum() > square_error:
        last_v =  v_pr
        v_pr= M_hat.dot(v_pr) 
    return v_pr
    


# In[11]:

pagerank(M_adj)


# In[61]:




# In[ ]:




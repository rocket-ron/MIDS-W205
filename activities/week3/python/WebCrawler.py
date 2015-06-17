
# coding: utf-8

# ## Reading a page from Web

# In[ ]:

import urllib


   
html=urllib.urlopen("http://ischool.berkeley.edu").read()
print html


# ## Downloading a file from Web
# 
# 

# In[ ]:

from PIL import Image

urllib.urlretrieve("http://www.ischool.berkeley.edu/sites/all/themes/ischool2008/ischool2008/images/logo_home.jpg","logo.jpg")

img = Image.open('logo.jpg')
img.show()


# ##Finding patterns in the downloaded page

# In[ ]:

import re

html=urllib.urlopen("http://www.ischool.berkeley.edu/people/faculty").read()

print re.findall('@[\w.]+', html)


# In[ ]:




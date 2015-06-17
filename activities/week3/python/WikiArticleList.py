
# coding: utf-8

# #Write a python program to process "enwiki-latest-stub-articles1.xml" file for the following tasks:
# 
# collect all page ids and title names for pages whose title starts with either "Afghanistan" or "America". Write this info into the file named pages.txt in the following format:
# 
# <page id>, <page title>

# In[6]:

import os
from xml.etree import ElementTree


# Load and parse an XML file
def parseXmlFile(fname):
	try:
		tree = ElementTree.parse(fname)		
	except Exception as inst:
		print ("error opening file: %s", inst)
		return
	return tree


def main():

	ftitle = open("pages.txt", 'w')
	
	tree = parseXmlFile("./enwiki-latest-stub-articles1.xml")
	if tree is not None:
		root = tree.getroot()		
		#to get the list of titles in all the docs
		count = 0
		for child in root.iter('page'):
			if child.find('title').text.startswith('Afghanistan') or child.find('title').text.startswith('America'):
				count += 1
				title_id = child.find('id')
				#print  child.find('id').text, child.find('title').text
				
				ftitle.write( child.find('id').text + "\t" + child.find('title').text  + "\n")
				
		ftitle.close()	
		

if __name__ == '__main__':
	main()
	


# In[7]:

get_ipython().system(u'cat pages.txt')


# In[ ]:




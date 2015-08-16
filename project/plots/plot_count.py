from boto.s3.connection import S3Connection
from boto.s3.key import Key
import string
import numpy as np
import matplotlib.pyplot as plt

conn = S3Connection()
bucket = conn.get_bucket("w205-rcordell-project")
b = conn.get_bucket(bucket)

cats = 'isis','ebola','trump','immigration','greece'
for graph in cats:
	f=""
	for key in bucket.list(prefix="emr/output/fearcounts/%s"%graph):
		# Search for the key that actually has output
	    contents = key.get_contents_as_string()
	    if len(contents)>0:
	        f=key.get_contents_as_string()
	        break


	f=f[6:]
	agg = f.split('], [')

	max_n = 25
	i = 0
	x, y = [], []
	for val in agg:
	    i+=1
	    if i>25:
	        break
	    tup = val.split(', ')
	    y.append(int(tup[0].lstrip("[")[0:]))
	    x.append(tup[1][1:].rstrip("\""))

	labels = x
	values = y

	ind = np.arange(max_n)
	width = 0.8
	plt.bar(ind+width/2,values,align = 'center')
	plt.ylabel('Fear Impressions')
	plt.xlabel('Twitter Username')
	plt.title('Top 10 fear disseminating users under the %s hashtag'%graph)
	plt.xticks(ind+width/2,labels, rotation = 'vertical')
	plt.tight_layout()
	plt.savefig('fc_%s'%graph+'.png')
	plt.clf()
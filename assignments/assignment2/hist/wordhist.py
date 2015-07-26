## Read the output of the EMR word count job and assemble the word counts
## into a dictionary that can then be used to plot a histogram of word
## frequencies for the top 30 words

from boto.s3.connection import S3Connection
from boto.s3.key import Key
import StringIO

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

conn = S3Connection(host="s3-us-west-1.amazonaws.com")
bucket = conn.get_bucket('W205-Assignment2-RC-emr'.lower())

# pull together the part-000XX files from the EMR job and assemble into a single
# dictionary for each search

w={}
for k in bucket.get_all_keys(prefix='out/warriors/part-'):
    part = StringIO.StringIO(k.get_contents_as_string())
    for line in part:
        (key,val) = line.split()
        w[key[1:-1]] = int(val)
part.close()
print len(w)

n={}
for k in bucket.get_all_keys(prefix='out/nbafinals/part-'):
    part = StringIO.StringIO(k.get_contents_as_string())
    for line in part:
        (key,val) = line.split()
        n[key[1:-1]] = int(val)
part.close()
print len(n)
b={}
for k in bucket.get_all_keys(prefix='out/both/part-'):
    part = StringIO.StringIO(k.get_contents_as_string())
    for line in part:
        (key,val) = line.split()
        b[key[1:-1]] = int(val)
print len(b)
part.close()
conn.close()

# plot the histogram of the top 30 word counts for each search

w_values = sorted(w.values(), reverse=True)[0:30]
w_keys = sorted(w, key=w.get, reverse=True)[0:30]

fig = plt.figure()
axw = fig.add_subplot(111)
width = 0.8
axw.bar(range(len(w_values)), w_values, width=width)
axw.set_xticks(np.arange(len(w_keys)) + width/2)
axw.set_xticklabels(w_keys, rotation=90)
plt.tight_layout()
#plt.show()
plt.savefig('warriors.png')

n_values = sorted(n.values(), reverse=True)[0:30]
n_keys = sorted(n, key=w.get, reverse=True)[0:30]

fig = plt.figure()
axn = fig.add_subplot(111)
width = 0.8
axn.bar(range(len(n_values)), n_values, width=width)
axn.set_xticks(np.arange(len(n_keys)) + width/2)
axn.set_xticklabels(n_keys, rotation=90)
plt.tight_layout()
#plt.show()
plt.savefig('nbafinals2015.png')

b_values = sorted(b.values(), reverse=True)[0:30]
b_keys = sorted(b, key=w.get, reverse=True)[0:30]

fig = plt.figure()
axb = fig.add_subplot(111)
width = 0.8
axb.bar(range(len(b_values)), b_values, width=width)
axb.set_xticks(np.arange(len(b_keys)) + width/2)
axb.set_xticklabels(b_keys, rotation=90)
plt.tight_layout()
#plt.show()
plt.savefig('both.png')
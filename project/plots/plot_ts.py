from boto.s3.connection import S3Connection
from boto.s3.key import Key
import string
from datetime import datetime
from matplotlib.dates import date2num
import matplotlib.ticker as mtick

import numpy as np
import matplotlib.pyplot as plt

conn = S3Connection()
bucket = conn.get_bucket("w205-rcordell-project")
b = conn.get_bucket(bucket)

cats = 'isis','ebola','trump','immigration','greece'
for graph in cats:
	f=""
	for key in bucket.list(prefix="emr/output/timeseries/%s"%graph):
	    contents = key.get_contents_as_string()
	    if len(contents)>0:
	        f+=key.get_contents_as_string()

	f = f.split("\n")
	# get rid of trailing line
	f.pop()
	x, y = [],[]
	resl = []
	for line in f:
	    foo = line.split('\t')
	    x_v = datetime.strptime(foo[0].strip("\""),"%m/%d/%y")
	    y_v = float(foo[1])*100
	    resl.append((x_v,y_v))
	resl.sort()
	x, y = zip(*resl)
	n = len(x)
	#x = date2num(x)


	labels = map(lambda _: datetime.strftime(_,"%m-%d-%y"),x)

	values = y

	ind = np.arange(n)
	width = 0.8

	plt.plot_date(ind+width/2,values, ls = '-')
	plt.ylabel('% Fearful Tweets')

	plt.xlabel('Date')
	plt.title('#%s Fear Trends'%graph,fontsize = 22)

	plt.xticks(ind+width/2,labels, rotation = 'vertical')

	fmt = '%.0f%%'
	yticks = mtick.FormatStrFormatter(fmt)
	plt.gca().yaxis.set_major_formatter(yticks)
	plt.gcf().autofmt_xdate()
	plt.tight_layout()
	plt.savefig('fig_ts_%s'%graph+'.png')
	plt.clf()
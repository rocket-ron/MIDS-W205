from boto.s3.connection import S3Connection
from boto.s3.bucket import Bucket
from boto.s3.key import Key
import datetime
import re

conn = S3Connection(host="s3-us-west-1.amazonaws.com")
tweetBucket = conn.get_bucket("w205-rcordell-project")

ts_re = re.compile(r'[a-zA-Z]+-[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}-([\d]{14})')
date_format = '%Y%m%d%H%M%S'

bucketInfo = [ 'isis', 'trump', 'greece', 'immigration' , 'TDF2015' , 'ebola' ]


totalSize = 0
for topic in bucketInfo:
	file_prefix = "data/twitter-streams/ebola-{0}".format(topic)
	keys = tweetBucket.list(prefix=file_prefix)
	chunkDates = []
	bytes = 0
	for key in keys:
		match = ts_re.search(key.name)
		if match:
			if match.group(1):
				chunkDates.append(datetime.datetime.strptime(match.group(1), date_format))
				bytes += key.size

	chunkDates.sort()
	duration = chunkDates[len(chunkDates) - 1] - chunkDates[0]

	totalSize += bytes

	print 'Topic: {0}'.format(topic)
	print 'Chunk count {0}'.format(len(chunkDates))
	print 'Tweet count {0}'.format(len(chunkDates) * 200)
	print 'Storage {0} MB'.format(bytes/(1024 * 1024))
	print 'Data ingest rate {0} MB/hr'.format((bytes/(1024 * 1024))/(duration.total_seconds()/3600))
	print '--------------------------------------------'

print 'Grand total storage in bucket: {0} MB'.format(totalSize/(1024*1024))
conn.close()



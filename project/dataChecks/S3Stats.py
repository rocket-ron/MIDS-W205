from boto.s3.connection import S3Connection
from boto.s3.bucket import Bucket
from boto.s3.key import Key
import datetime

conn = S3Connection(host="s3-us-west-1.amazonaws.com")
tweetBucket = conn.get_bucket("w205-project-twitter-streams")

date_format = '%Y-%m-%dT%H:%M:%S.000Z'

bucketInfo = [ 'isis', 'trump', 'greece', 'immigration' , 'TDF2015' , 'ebola' ]
totalSize = 0
for topic in bucketInfo:
	keys = tweetBucket.list(prefix=topic)
	chunkDates = []
	bytes = 0
	for key in keys:
		chunkDates.append(datetime.datetime.strptime(key.last_modified, date_format))
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



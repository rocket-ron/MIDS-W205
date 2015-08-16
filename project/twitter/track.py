#!/usr/bin/python

from twitterutils.apikeys import apikeys
from twitterutils.trackerListener import TrackerListener
from serializers.mongoTweetSerializer import MongoTweetSerializer
from serializers.s3ChunkedTweetSerializer import S3ChunkedTweetSerializer
from serializers.consoleTweetSerializer import ConsoleTweetSerializer
import argparse
import time


parser = argparse.ArgumentParser(description = 'Track phrases in the Twitter stream API and serialize them to a destination',
								 add_help=True,
								 formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--key',
					type=str,
					required=True,
					choices=apikeys.keys(),
					help='the Twitter API key to use')
parser.add_argument('--track',
					type=str,
					required=True,
					help='Twitter phrases to track')


mongoGroup = parser.add_argument_group("mongoDB", "Parameters used for MongoDB serialization")
mongoGroup.add_argument('--db',
					type=str,
					required=False,
					default=None,
					help='MongoDB database to store tweets')
mongoGroup.add_argument('--col',
					type=str,
					required=False,
					default=None,
					help='MongoDB collection to store tweets')
mongoGroup.add_argument('--svr',
					type=str,
					required=False,
					default='127.0.0.1',
					help='MongoDB server host name or ip address')

s3Group = parser.add_argument_group("s3", "Parameters used for AWS S3 serialization")
s3Group.add_argument('--bucket',
					type=str,
					required=False,
					default=None,
					help='Amazon S3 storage to store tweets')
s3Group.add_argument('--chunks',
					type=str,
					required=False,
					default=100,
					help='number of tweets per chunk for S3 buckets')

args = parser.parse_args()


fetchSize = 1500

# pick the serializer
if args.db:
	if (args.col):
		print "Writing tweets to MongoDB..."
		serializer = MongoTweetSerializer(args.svr, args.db , args.col)
	else:
		print "MongoDB database and collection must be specified when using MongoDB server"
		sys.exit(1)
elif args.bucket:
	"Writing tweets to S3 bucket " + args.bucket + " ..."
	serializer = S3ChunkedTweetSerializer(args.chunks, args.track.replace(" ",""), args.bucket)
else:
	print "Writing tweets to console..."
	serializer = ConsoleTweetSerializer()
	fetchSize = 10

startTime = time.time()

listener   = TrackerListener(serializer, apikeys[args.key])
listener.track(args.track)

print "Tracking stopped after " + str(time.time() - startTime) + " seconds."



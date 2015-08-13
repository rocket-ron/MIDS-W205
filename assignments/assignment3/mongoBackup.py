import subprocess
import tarfile
import time
import os
import math
import argparse

from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.key import Key
from filechunkio import FileChunkIO

# backup all the databases in the local instance

parser = argparse.ArgumentParser(description = "Backup and Restore Single Instance Mongo Database")
parser.add_argument('-s', '--server',
					type=str,
					required=False,
					default='127.0.0.1',
					help='MongoDB server to backup. Default is 127.0.0.1')
parser.add_argument('-o', '--out',
					type=str,
					required=False,
					default='./dump',
					help='local directory to store backup. Default is current working directory')
parser.add_argument('-d', '--database',
					type=str,
					required=False,
					default=None,
					help='MongoDB database to backup. Default is to backup all of them on the instance')
parser.add_argument('-b','--bucket',
					type=str,
					required=False,
					default=None,
					help='S3 bucket name to upload backup. Default is not to upload to S3')
parser.add_argument('-a', '--action',
					type=str,
					required=False,
					default='backup',
					choices=['backup','restore'],
					help='indicates backup or restore operation')
parser.add_argument('-t', '--test',
					type=bool,
					required=False,
					default=False,
					const=True,
					nargs='?',
					help='output command parameters and exit with no action')
parser.add_argument('-i', '--infile',
					type=str,
					required=False,
					default=None,
					help='restore file name. If S3 bucket is specified, the file in the S3 bucket')


def backup(args):
	timeString = time.strftime('%Y%m%d%H%M%S')
	cmd = 'mongodump --host ' + args.server + ' --out ' + args.out

	if args.database:
		cmd += ' -d ' + args.database

#	cmd='mongodump --host 192.168.194.171'

	if args.test:
		print "mongodump command string = " + cmd
	else:
		print "Executing mongodump command on server " + args.server
		subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

		fname = 'mongoBackup-' + timeString
		fname += '.tar.gz'
		print "Compressing mongodump output to " + fname

		tar = tarfile.open(fname, 'w:gz')
		tar.add(args.out, arcname="mongoBackup")
		tar.close()

	if args.bucket:
		_bucket = args.bucket.lower() + '-' + timeString

		if args.test:
			print "S3 bucket would be: " + _bucket
		else:
			print "Uploading " + fname + ' to S3 bucket ' + _bucket
			conn = S3Connection(host="s3-us-west-1.amazonaws.com")
			bucket = conn.create_bucket(_bucket, location=Location.USWest)
			bucket.set_acl('public-read')

			source_size = os.stat(fname).st_size
			mp = bucket.initiate_multipart_upload(os.path.basename(fname))

			chunk_size = 52428800
			chunk_count = int(math.ceil(source_size / float(chunk_size)))

			for i in range(chunk_count):
				offset = chunk_size * i
				bytes = min(chunk_size, source_size - offset)
				with FileChunkIO(fname, 'r', offset=offset, bytes=bytes) as fp:
					mp.upload_part_from_file(fp, part_num=i + 1)

			mp.complete_upload()
			conn.close()

# CAUTION - restore operation is not fully tested
def restore(args):
	if args.infile:
		_path = getS3(args)
		if _path:
			tar = tarfile.open(_path, 'r:gz')
			tarfile.extractall()
			tarfile.close()

			cmd = 'mongorestore --host ' + args.server 
			if args.database:
				cmd += ' --database ' + args.database 
			cmd += ' ' + _path
	else:
		print "Unable to restore if restore file name is not specified"
		return -1

def getS3(args):
	if args.bucket:
		print "Downloading " + args.infile + ' from S3 bucket ' + args.bucket
		conn = S3Connection(host="s3-us-west-1.amazonaws.com")
		bucket = conn.get_bucket(args.bucket.lower())
		key = bucket.get_key(args.infile)
		with open(args.infile, 'w') as f:
			key.get_contents_to_file(f)
		f.close()
		k.close()
		conn.close()
		return infile
	else:
		return None

if __name__ == '__main__':
	args = parser.parse_args()

	if args.action == 'restore':
		restore(args)
	else:
		backup(args)
## AWS EMR mrcc job
##
## Process the tweet data gathered and stored in AWS S3. Filenames will be provided via the invocation
## Count the words in all of the tweets across all the .json files in the S3 location
##
## to run the mrcc job, do the following:
##
## 1. tar -cvzf mrcc.py.tar.gx mrcc.py
## 2. make sure the tar file is in the mrjob directory
## 3. python word_count.py -r emr --conf-path mrjob.conf --python-archive mrcc.py.tar.gz --no-output --output-dir s3://bucket-name --source s3 input input/inputfile
## Make sure the inputfile has the list of bucket keys to include (filenames)


import gzip
#
import boto
import json
#
from boto.s3.key import Key
from mrjob.job import MRJob

class CCJob(MRJob):
  def process_record(self, record):
    """
    Override process_record with your mapper
    """
    raise NotImplementedError('Process record needs to be customized')

  def configure_options(self):
    super(CCJob, self).configure_options()
    self.add_passthrough_option('--source',help="Provide the source of the data")


  def mapper(self, _, line):
    f = None
    ## If we're on EC2 or running on a Hadoop cluster, pull files via S3
    if self.options.source in ['s3']:
      # Connect to Amazon S3 using anonymous credentials
      conn = boto.connect_s3()
      pds = conn.get_bucket('w205-assignment2-rc-data')
      # Start a connection to one of the JSON files
      # In this case, pds is the S3 bucket and line is the key
      # because the "lines" are from the input file where each line is a key name
      k = Key(pds, line.rstrip())
      chunk = json.loads(k.get_contents_as_string())
    ## If we're local, use files on the local file system
    else:
      print 'Loading local file {}'.format(line)
      with open(line) as data_file:
        data = data_file.read()
        chunk = json.loads(data.decode("utf-8"))
    ###
    try:
      for tweet in chunk:
        for key, value in self.process_record(tweet):
          yield key, value
        self.increment_counter('twitter', 'processed_tweets', 1)
    except Exception as e:
      return

  # TODO: Make the combiner use the reducer by default
  def combiner(self, key, value):
    yield key, sum(value)

  def reducer(self, key, value):
    yield key, sum(value)


 
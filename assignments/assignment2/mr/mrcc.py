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


 
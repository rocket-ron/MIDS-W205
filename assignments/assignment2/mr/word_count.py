##
## Simple word counter
##

from collections import Counter
###
from mrcc import CCJob


class WordCount(CCJob):
  def process_record(self, tweet):
    data = tweet[u'text']
    if data == None:
      return

    #for word in data.split():
    #  yield word, 1
    for word, count in Counter(data.split()).iteritems():
      yield word, 1
    self.increment_counter('twitter', 'processed_record', 1)

if __name__ == '__main__':
  WordCount.run()

import re
from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    # extract the tweet text from the CSV file, in the 5th field
    # strip out all but alphanumeric and whitespace
    # split apart into words and yield as key, value
    def mapper(self, _, line):
        tweet=line.split("|")[4].lower()
        tweet=re.sub(r'[^a-zA-Z0-9\s]','', tweet)
        words=tweet.split()
        for word in words:
            yield word, 1

    # Accumulate the key, values and filter out accumulations < 10K
    def reducer(self, key, values):
        total=sum(values)
        if total>10000: 
            yield key, total

if __name__ == '__main__':
    MRWordFrequencyCount.run()

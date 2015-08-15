import time
from mrjob.job import MRJob

class MRTimeBucketCount(MRJob):

    # extract the time in seconds since epoch from the CSV file, in the 6th field
    # convert to a time_struct (the file has already been checked for invalid fields)
    # create a tuple (month, day, hour) as the key and value of 1
    def mapper(self, _, line):
        t = line.split("|")[5].lower()
        if t != 'time':
            tm = time.gmtime(int(t))
            month = str(tm.tm_mon)
            day = str(tm.tm_mday).zfill(2)
            hour = str(tm.tm_hour).zfill(2)
            yield (month, day, hour), 1

    # Accumulate the key, values 
    def reducer(self, key, values):
        total=sum(values)
        yield key, total

if __name__ == '__main__':
    MRTimeBucketCount.run()

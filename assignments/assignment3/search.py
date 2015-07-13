import sys
import datetime
import urllib
import tweetFetcher

# time and date formats
xsdDatetimeFormat = "%Y-%m-%dT%H:%M:%S"
xsdDateFormat = "%Y-%m-%d"

def datetime_partition(start,end,duration):
   current = start
   while start==current or (end-current).days > 0 or ((end-current).days==0 and (end-current).seconds>0):
      yield current
      current = current + duration
      
def date_partition(start,end):
   return datetime_partition(start,end,datetime.timedelta(days=1))

# if __name__ == "__main__":
#   start = datetime.datetime.strptime(sys.argv[1],xsdDateFormat) # start date
#   end = datetime.datetime.strptime(sys.argv[2],xsdDateFormat)   # end date
   
#   for d in date_partition(start,end):
	

q = urllib.quote(sys.argv[1])
# q = sys.argv[1]

if (len(sys.argv) > 2):
	if (sys.argv[2] != None):
		start = datetime.datetime.strptime(sys.argv[2],xsdDateFormat) # start date
		q = q + " since:" + start.strftime(xsdDateFormat)

if (len(sys.argv) > 3):
	if (sys.argv[3] != None):
		end = datetime.datetime.strptime(sys.argv[3],xsdDateFormat)   # end date
		q = q + " until:" + end.strftime(xsdDateFormat)

print q

fetcher = tweetFetcher.TweetFetcher()
fetcher.search(q)
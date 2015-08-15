# W205 Summer 2015 Assignment 4

## FIFA Women's World Cup 2015 Tweet Gathering

### Objective:
Write an acquisition program that can acquire the tweets between June 6th and July 5th of 2015 for the official FIFA Women World Cup hashtag (“#FIFAWWC”), as well as team code hashtags (e.g. “#USA” and “#GER”) and store them with appropriate structures in WC2015.csv on S3.

### Solution:
To acquire historical tweets for the FIFA WWC event requires using the [Twitter web search](http://twitter.com/search). Historical tweets are not available from the Twitter REST API. Therefore a web screen scraper is required to harvest the tweets.

The `fifa.py` program performs the web-scraping function against the Twitter search web page. The program consists of two parts: setting up the initial search using the query, and then paging through the results. The scraper mimics what happens when a user interacts with the search through a browser, scrolling down to get the next page of tweets. Each page is loaded via an AJAX call back to the Twitter search server and placed on the web page as a set of HTML list elements, about 20 tweets per "page". The second part of the program is identical to the first except that instead of sending the initial query, the parameters necessary for the AJAX call are sent instead. The AJAX parameters consist of the query, the type of response, the language and the current position in the pages of tweets as given by the last tweet id.

The scraper extracts the tweets using the Beautiful Soup Python module to locate the HTML list items that contain the tweets and associated metadata. The information is written in CSV format to a local file. The extracted information from the HTML is:
 - tweet id
 - user id
 - user name
 - screen name
 - tweet text
 - time (seconds since epoch)
 
The output file is located [on S3](httpds://w205-rcordell-assignment4.s3.amazonaws/WC2015.csv). The CSV uses a delimiter of '|' so as to preserve some of the punctuation in the tweet text which may be commas. The file contains 128,948 entries.

### Data Cleanup:
#### Pesky Carriage Returns and Line Feeds
After the CSV file was created it was found that the tweet texts contain carriage return `\r` and line feed `\n` characters, breaking the CSV format. Unfortunately this was not considered in the original parsing and storage, so the CSV file required a clean-up step. The `CleanCSVFile.ipynb` is an IPython notebook used to explore and clean the data. Fortunately an algorithm to clean up the data is compact and straightforward to write.

#### Those Dang Twitter Users use the | in Their Tweets and Screen Names!
When it came time to run the Map Reduce job for Part 2 of the assignment where we count the number of tweets per hour, I found that there were extra `| `characters in the CSV file. This happened because user screen names might be something clever like `|| Big Mike ||` or even `|_|-|\ Dude /|-|_|`. Also, several tweets had the `|` in the text to call out scores and such. I wrote another cleaning program to search for these cases and merge the fields, and then check the final output file to make sure it had exactly 5 fields per line. This is the `DelimiterCleaning.ipynb` notebook and produces a separate output file that is then copied to S3 to replace the original one.

### Task 1
Write a map-reduce program that counts the number of words with more than 10000 occurrences.

### Solution:
The `wordFrequencyCount.py` program is an MRJob-based class that runs on AWS EMR spot instances to compute the word counts using map reduce jobs. The output of the job is located [here](https://w205-rcordell-assignment4.s3.amazonaws.com/problem1/part-00000) and contains the following word counts:

Word    | Count
------- | --------
"a"     | 25837
"and"   |  16387
"at"    |  12962
"aus"   | 12003
"can"   | 22907
"eng"   | 30663
"fifawwc" |  130069
"for"   |  22122
"game"  | 12309
"ger"   |  22386
"in"    |  25951
"is"    |  14803
"jpn"   | 11172
"of"    |  16967
"on"    |  18484
"the"   |  62327
"this"  | 11449
"to"    |  34012
"usa"   |  54448

### Task 2
Write a map-reduce program to compute the tweet volume on an hourly basis (tweets/hour)

### Solution:
The program `timeBucketCount.py` creates an MRJob map-reduce class to compute the number of tweets per time bucket. The CSV file contains the seconds-since-epoch as the last field in an entry. This value is used to create a `struct_time` object from which the year, month and day are easily computed. The year, month, day are converted to strings and used to create a tuple of `(year, month, day)`, which is yielded with a count of 1. The reducer uses the tuple as the key to accumulate the values. The output is located [here](https://w205-rcordell-assignment4.s3.amazonaws.com/problem2/part-00000). A sample of the output is below:


*Times are GMT*

Day  | Hour | Tweets
-----|------|-------
6/05 | 00  |    9
6/05 | 01  |    13
6/05 | 02  |    26
6/05 | 03  |    13
6/05 | 04  |    10
6/05 | 05  |    8
6/05 | 06  |    7
6/05 | 07  |    6
6/05 | 08  |    13
6/05 | 09  |    5
6/05 | 10  |    5
6/05 | 11  |    13
6/05 | 12  |    15
6/05 | 13  |    19
6/05 | 14  |    21
6/05 | 15  |    40
6/05 | 16  |    28
6/05 | 17  |    30
6/05 | 18  |    41
6/05 | 19  |    24
6/05 | 20  |    26
6/05 | 21  |    39
6/05 | 22  |    29
6/05 | 23  |    27
6/06 | 00  |    26
6/06 | 01  |    16
6/06 | 02  |    19
6/06 | 03  |    41
6/06 | 04  |    39
6/06 | 05  |    18
6/06 | 06  |    7
6/06 | 07  |    18
6/06 | 08  |    10
6/06 | 09  |    12
6/06 | 10  |    29
6/06 | 11  |    28
6/06 | 12  |    66
6/06 | 13  |    106
6/06 | 14  |    115
6/06 | 15  |    110
6/06 | 16  |    102
6/06 | 17  |    73
6/06 | 18  |    67
6/06 | 19  |    95
6/06 | 20  |    102
6/06 | 21  |    394
6/06 | 22  |    704
6/06 | 23  |    1000

### Task 3
Write a map-reduce program to compute the top 20 URLs tweeted by the users


### Solution
The `urlFrequencyCount.py` map-reduce program uses a public domain regular expression to find and extract URLs from the tweets. The URL is used as the key and emitted with a count of 1; the reducer accumulates by the key to create the total URL count. The complete output is in [S3 here](https://w205-rcordell-assignment4.s3.amazonaws.com/problem3/part-00000). The top 20 URLs are:

URL                                 |   Count
------------------------------------|--------------
"http://ift.tt/1BogwgX"             | 3771
"http://WWW.FIFANEWS.CA"            | 1136
"http://goo.gl/gy1ctl"              | 136
"http://bbc.in/1mbSmuT"             | 70
"https://goo.gl/ksK82F"             | 66
"http://bit.ly/1C8YzQz"             | 60
"http://soccer-aloud.com"           | 55
"http://bit.ly/1JZZedN"             | 49
"http://bbc.in/1MzvS5F"             | 43
"http://fifa.to/1Kpov2F"            | 43
"http://bbc.in/1NtaSxJ"             | 40
"http://playerpress.com"            | 40
"http://bit.ly/1J9juJB"             | 35
"http://bbc.in/1Jol6B7"             | 33
"http://goo.gl/bwQkZS"              | 33
"https://blog.twitter.com/2015/preview-usa-vs-jpn-in-the-fifawwc-final"  | 33
"http://bbc.in/1KnMXjj"             | 32
"http://twitter.com/Gotham/status/  |
  607979128755621888/photo/1pic.twitter.com/79T5w0UXsL" | 32
"http://bit.ly/womenwc15"  | 31
"http://fifa.to/1eMW81u"   | 31
"pic.twitter.com/10XPQumVOn"  |  31
"http://fifa.to/1H5LLlI"   | 30
"http://wp.me/p4msBw-5iq"  | 30
"http://www.sbnation.com/soccer/2015/6/22/8826981/norway-england-final-score-2015-world-cup-results-lucy-bronze"  |  30


### Task 4
Write a map-reduce program to compute word association counts.


### Solution
The `wordAssociationCount.py` map reduce program takes each tweet and first removes all URLs. Then the remaining content is tokenized using a regular expression that allows only alphanumeric characters and underscore `\w`. The terms form a list used by two iterators to create word pairings. Each word pair forms a tuple: `(word1, word2)` and is used as the key and emitted with a count of 1 from the mapper generator function. 

I considered whether to combine keys so that `(word1, word2` and `(word2, word1)` would be combined into a common count. I implemented this using a simple comparator when creating the tuple so that if `word 1 >= word2` the tuple is created with that order, or reversed otherwise. However I decided to leave it without that because the instructions appeared to read otherwise. Looking at the output makes me think I should've left it in. 

I also tried to use a multi-step reducer so that the final output is sorted by the pair counts but couldn't get it to work. In the interest of time I created an IPython notebook, `Top20WordAssociations.ipynb` to build a sorted list from the S3 EMR output files, although this wasn't strictly necessary.

The output files of the map-reduce job is in [S3 here](https://w205-rcordell-assignment4.s3.amazonaws.com/problem4/).

Eaxmple output is below:


Word Pair           |   Count
--------------------|-----------
('the', 'FIFAWWC') | 57038
('FIFAWWC', 'the') | 57038
('FIFAWWC', 'USA') | 53825
('USA', 'FIFAWWC') | 53825
('FIFAWWC', 'to') | 33859
('to', 'FIFAWWC') | 33859
('FIFAWWC', 'ENG') | 28221
('ENG', 'FIFAWWC') | 28221
('FIFAWWC', 'in') | 25567
('in', 'FIFAWWC') | 25567
('the', 'to') | 23843
('to', 'the') | 23843
('FIFAWWC', 'a') | 23640
('a', 'FIFAWWC') | 23640
('FIFAWWC', 'GER') | 22115
('GER', 'FIFAWWC') | 22115
('USA', 'the') | 21737
('the', 'USA') | 21737
('for', 'FIFAWWC') | 21731
('FIFAWWC', 'for') | 21731

## Questions

### Average Length of Tweets

    print float(accum['characters'])/float(accum['line'])
    92.3614219422

### Team Support Table

Team hashtag |  Count
-------------|---------
"#AUS" | 12092
"#BRA" | 3167
"#CAN" | 19991
"#CHN" | 4989
"#CIV" | 2852
"#CMR" | 2443
"#COL" | 5111
"#CRC" | 1270
"#ECU" | 1517
"#ENG" | 31024
"#ESP" | 1465
"#FRA" | 8876
"#GER" | 22656
"#JPN" | 11415
"#KOR" | 2180
"#MEX" | 2297
"#NED" | 3690
"#NGA" | 4742
"#NOR" | 4684
"#NZL" | 2211
"#SUI" | 3264
"#SWE" | 5200
"#THA" | 2170
"#USA" | 52182


### How many times does 'USA' occur with 'Japan'

    print assoc[('USA','Japan')]
    1030

### How many times does 'champion' occur with 'USA'

    print assoc[('champion', 'USA')]
    24

    print assoc[('champions', 'USA')]
    64

## Twitter Archive Search

### Whoosh Indexer
The IPython notebook `Indexer.ipynb` was used to create the Whoosh index. The index schema consists of:

    schema = Schema(content=TEXT(stored=True), 
                tweetid=ID(stored=True), 
                user=TEXT(stored=True), 
                userid=ID(stored=True), 
                date=DATETIME(stored=True))

The `content` field contains the tweet text
The `tweetid` field contains the tweet id
The `user` field contains the user name
The `userid` field contains the user id
The `date` field contains the `datetime` of the tweet

The Whoosh index files are located [on S3](https://w205-rcordell-assignment4.s3.amazonaws.com/whoosh/)



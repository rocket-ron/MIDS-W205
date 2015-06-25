# W205 Assignment 2 #
## Ron Cordell, Summer 2015 ##

The purpose of Assignment 2 is to capture twitter data for three different cases:
 1. Tweets with the hashtag #NBAFinals2015 but not #Warriors
 2. Tweets with the hashtag #Warriors but not #NBAFinals2015
 3. Tweets with both hashtags

## Setup ##

### Data Acquisition ###

Using a modified form of the twitter search code from the Twitter search Activity, perform searches for the data required.
The searches were performed with the Tweepy search API. Each search used a Cursor to fetch 1500 tweets at a time and serialize
them to a file in AWS S3 storage.

The searches performed were:
 1. "#NBAFinals2015 -#Warriors since:2015-06-10 until:2015-06-20"
 2. "#Warriors -#NBAFinals2015 since:2015-06-10 until:2015-06-20"
 3. "NBAFinals2015 #Warriors since:2015-06-10 until:2015-06-20"

The search timeline was deliberately more than 7 days in order to capture as much data as possible. The actual data captured ranged
from 2015-06-14 to 2015-06-19

### Data Chunking and S3 Storage ###

Tweets resulting from the search were stored in AWS S3 in .json files with 200 tweets per chunk. This was chosen because the raw data
is about 1MB in size which allows for a good size file without having to transmit too much at one time across the network. It also is
small enough that a big gap in the data would not occur if a chunk was lost. A python script was used to scan the tweet dates in all
the captured chunks to analyze for data gaps and to correct where needed, but it was not necessary to correct any gaps.

The S3 storage location is in the us-west-1 region, with the bucket name 'w205-assignment2-rc-data', which has been made publicly
accessible.

The chunked output from each search is in a subfolder per search:
 -NBAFinals2015
 -Warriors
 -WarriorsAndNBAFinals2015

## Word Count Analysis ##

### Elastic Map Reduce ###

In one scenario, word counts were performed with AWS EMR as submitted via mrjob. The resulting word count output was placed in S3 storage.
Final processing was performed by creating a dictionary for each search then plotting the top 30 word counts as a histogram or bar
chart. No stop word filtering was done. The graphed output is available as 
 1. nbafinals2015.png
 2. warriors.png
 3. both.png

### Warriors ###
![Warriors Search](https://github.com/rocket-ron/MIDS-W205/blob/assignment2/assignments/assignment2/hist/Warriors.png "#Warriors")

### NBAFinals2015 ###
![NBAFinals2015 Search](https://github.com/rocket-ron/MIDS-W205/blob/assignment2/assignments/assignment2/hist/NBAFinals2015.png "#NBAFinals2015")

### Warriors and NBAFinals2015 ###
![Warriors and NBAFinals2015 Search](https://github.com/rocket-ron/MIDS-W205/blob/assignment2/assignments/assignment2/hist/both.png "#Warriors and #NBAFinals2015")

### NLTK Tokenizer ###

In the second scenario the Twitter .json files were processed by a simple Python script that extracts the tweet text for any english 
language tweet, strips punctiation using the nltk RegexpTokenizer and filters for the nltk english stop word list. The stop word list
was augmented with a few extra strings: http, https, co, the numerals 1 - 9. The resulting word list was plotted using the Frequency
word plot available in the nltk module. The resulting word plots are:
 1. Both_nltk.png
 2. Warriors_nltk.png
 3. NBAFinals2015.png

### Warriors (NLTK) ###
![Warriors Search](https://github.com/rocket-ron/MIDS-W205/blob/assignment2/assignments/assignment2/hist/Warriors_nltk.png "#Warriors")

### NBAFinals2015 (NLTK) ###
![NBAFinals2015 Search](https://github.com/rocket-ron/MIDS-W205/blob/assignment2/assignments/assignment2/hist/NBAFinals2015_nltk.png "#NBAFinals2015")

### NBAFinals2015 and Warriors (NLTK) ###
![Warriors and NBAFinals2015 Search](https://github.com/rocket-ron/MIDS-W205/blob/assignment2/assignments/assignment2/hist/Both_nltk.png "#Warriors and #NBAFinals2015")

 ## Conculusions ##

 The EMR process was interesting and simple, but with only ~475K tweets to process was overkill and took a lot of time to spin up an 
 EMR cluster. 

 The NLTK library was easy to use and contains all the tools necessary to process the tweet texts with the addition of the stop word 
 filter. However, the stop word filter may be too extensive for tweets, especially for sentiment analysis. With 140 characters in a 
 tweet, even articles carry extra information. It is interesting to compare the results of the histograms.


# Assignment 3 #

## Storing Tasks ##

### 1.1 Retrieve and store JSON files from the Twitter REST API to a MongoDB database called db_restT
This part of the assignment was actually left as the result of Assignment 2 where the NBAFinals and Warriors Twitter searches resulted in a set of S3 files containing chunked JSON tweets. The S3 files were not moved to a MongoDB database because **1.2** requires pulling the data from the S3 files. It is assumed that **1.1** makes sense to do if pulling the data from the Twitter REST API the first time.

### 1.2 Insert the chunked tweets into a MongoDB database 
A Python program was created to pull the chunked tweets from the S3 files and store them in a locally created MongoDB database. The Python program is called `retrieveTweets.py`. Using the AWS credentials provided in the user environment variables, a connection is made to the S3 bucket that contains 3 folders: tweets for the `#NBAFinals2015`, `#Warriors`, and `#NBAFinals OR #Warriors`. The data files were gathered during the NBA Finals as part of Assignment 2.

The `retrieveTweets.py` program accesses each folder and iterates through all the keys in the bucket that end in '.json'. The JSON that constitutes the chunked JSON tweets is loaded and then inserted into the MongoDB database using an `insert_many(chunk)` for efficiency. The result is that the MongoDB collection contains all of the tweets gathered from the three buckets.

NOTE: Although the directions indicate using a database called `db_tweets`, the actual database used was `db_restT` and the collection called `restT`. This was because of some confusion over the first two steps of the assignment, but it didn't seem to be necessary to move the data or rename the databases/collections.

## Retrieving and Analyzing Tasks ##

### 2.1 The Top 30 Retweets
A Python program was written to compute the top 30 retweets contained in the collection of all the NBA Finals tweets, called `extractRetweets.py`. 

This program uses the MongoDB aggregation pipeline to:
 - `$match` all english retweets to filter out non-english retweets
 - `$group` uniquely on the tweet id of the retweeted tweet 
    - gather the
        - `userid` (the author of the retweeted tweet)
        - `name`
        - `screen_name`
        - `location`
        - `text` (the text of the retweeted tweet)
    - `$sum` the number of times the tweet has been retweeted
 - `$sort` in descending order on the aggregated count (sum)
 - `$limit` to the first 30 (giving us the top 30)
 - `$out` store the resulting list to a collection called 'retweets'

The aggregation is a single "statement". Indexes have been created on the fields of `lang`, and `retweeted_status.id_str` from the MongoDB shell.

### 2.2 Compute the Lexical Diversity of the users of all tweets
This step is one of the reasons the tweet data was placed in the db_restT database and left there from step **1.2**. To extract all the users from all the tweets gathered and compute the lexical diversity of each user's tweet corpus the program `userTimeline.py` was created. This program uses a similar pattern to other Tweet REST API programs created for previous assignments in that there is the main program `userTimeline.py` that uses a `TimelineFetcher` class to fetch the user timeline and a `MongoTweetAnalyzer` to perform the analysis and store the results.

The `userTimeline.py` program performs a MongoDB search for distinct user id's from the `restT` collection (where the tweets are stored) and filters for english only. The list of user ids is then fed into the `TimelineFetcher` class which uses a Tweepy `Cursor` object to query the Twitter REST API for the user's timeline of the most recent 3200 tweets (the maximum allowed via this API). The text of all the tweets are gathered, filtered for urls with a regex and fed to the `MongoTweetAnalyzer` class. The `MongoTweetAnalyzer` class uses the NTLK library's stop words and extends them for things like 'rt', 'co', single digit numerals, etc. The resulting text is tokenized, resulting in a List of tokens, which is used to create a Counter() instance, which does the work of accumulating similar words into a dictionary with the word counts. Finally the lexical diversity is calculated as the total number of unique words divided by the total number of words.

The Counter class is used as the postings element of a dictionary, along with the Twitter user_id, word count and unique word count and computed diversity score. The resulting dictionary is stored in the MongoDB collection called `lexdiv`. The structure of the documents in the `lexdiv` collection is:

    { user_id       : string (64-bit integer string representation), 
      word_count    : integer, 
      unique_count  : integer,
      diveristy     : float (ranges from 0 - 1),
      postings      : dict/sub document
        { term : count }
    }


The program has been running continuously since June 16 and has gathered the lexical diversity of 6056 users out of a total of over 220,000 as of noon on June 19. The program outputs the list of users gathered thus far so that if it requires a restart those users will be excluded.

The program `lexicalDiversity.py` is used to query the `lexdiv2` collection of computed lexical diversity scores and graph the results. Two graphs were computed: a histogram of the lexical diversity of the 6000+ users, and a scatterplot of lexical diversity by follower count. The scatterplot cuts off follower counts > 2000 in order to show the most information, since the largest number of followers for the users is > 3 million.

#### Lexical Diversity of the 6000+ Users

[insert graphic here]

#### Lexical Diversity by Follower Count

[insert graphic here]

### 2.3 Followers of the Top 30 Retweeters
This part of the assignment has been the most difficult to practically implement because the API that returns followers is not particularly fast. When a Twitter user has a lot of followers it can take days to retrieve all them; in fact for the #1 retweeter from **2.1** all the followers are still being gathered. This is despite using three Twitter API keys to run parallel isntances of the follower gathering code. Because of this limitation, it is not practical to perform a delta of followers. I could have made the choice to limit the number of followers to 100 (or some number) per user, but it's an arbitrary and essentially meaningless thing to do considering the topic of the assignment. If I had more time I would have changed my strategy to rotate Twitter API keys such that when a timeout rate limit is hit using one set of keys, the program uses the last returned follower id to query from that point under a different set of keys. In this way the time gaps can be eliminated and the retrieval process sped up. But as I said, I'm out of time to implement it. In fact, even starting with the #30 in the top 30 list it took 48 hours to pull all the followers. Therefore only this user will have a true follower delta calculated.

To gather followers the same pattern of Python modules is used: `followers.py` starts things off. It either uses the userId from the command line or if none is present will query the MongoDB for the list of user ids. This is passed to the `FollowerFetcher` class which queries the Twitter REST API for the followers of a particular user. The resulting list of Tweepy `User` objects is passed to the `MongoFollowerSerializer` class which writes the follower information to the `follower` collection. The structure used for the document is:

    { user          : string (the user who is followed),
      id_str        : string (the user who is following),
      name          : string (the Twitter name of the follower),
      screen_name   : string (the Twitter screen name of the follower)
    }

When a second pass is made to find the followers of a user, the `user` field entry is appended with `-2`. Therefore there are essentially two lists representing two result sets that can be operated on with a `NOT AND` type of search to find the ones that were added or dropped.

In addition to this exercise, the original `lexdiv` collection was amended with a new field for the `follower_count` of the Twitter user. Since this was done after the intial data gathering from Twitter, the data from the `lexdiv` collection was queried, the Twitter API queried for the number of followers for a user and the new field added to the dictionary, then the dictionary written as a document to a new collection called `lexdiv2`. From this we are able to obtain the total number of followers for the users for which we've already pulled the follower details and use it to order the histogram of lexical diversity.

### 2.4 Sentiment Analysis

TBD

## Storing and Retrieving Task - MongoDB backups

### 3.1 Write a Python program to backup MongoDB databases to S3

The `mongoBackup.py` program uses the `subprocess` Python module to invoke the mongodump utility to dump the monogdb contents to a specified location. This location is then compressed into a gzip'ed tar file named `mongoBackup-` then the current time. For example, `mongoBackup-201507192205344.tar.gz`. Finally, the compressed file is uploaded to an S3 bucket named `w205-rlc-mongobackups` with the same time stamp appended. Chunked file IO is used to upload the file as it is several GB or more in size.The S3 bucket is set to `public-read`.

[This is the backup taken at 2015-07-19 22:13:47](https://s3-us-west-1.amazonaws.com/w205-rlc-mongobackups-20150719221347/mongoBackup-20150719221347.tar.gz)

The `mongoBackup.py` program has a number of command line arguments. The output of the help command gives the information about the arguments:

    Backup and Restore Single Instance Mongo Database

    optional arguments:
      -h, --help            show this help message and exit
      -s SERVER, --server SERVER
                            MongoDB server to backup. Default is 127.0.0.1
      -o OUT, --out OUT     local directory to store backup. Default is current
                            working directory
      -d DATABASE, --database DATABASE
                            MongoDB database to backup. Default is to backup all
                            of them on the instance
      -b BUCKET, --bucket BUCKET
                            S3 bucket name to upload backup. Default is not to
                            upload to S3
      -a {backup,restore}, --action {backup,restore}
                            indicates backup or restore operation
      -t [TEST], --test [TEST]
                            output command parameters and exit with no action
      -i INFILE, --infile INFILE
                            restore file name. If S3 bucket is specified, the file
                            in the S3 bucket

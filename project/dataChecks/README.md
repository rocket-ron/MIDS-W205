# Processing Data and Ensuring Data Integrity

## Explanation of Contents

This directory contains various tools and working items to help manage the data collected, whether in S3 or MongoDB. Most of the code is used to discover data gaps in time, de-duplicate data, filter data, and move data from one place to another. Some of the tools are for a more interactive medium like IPython, and some tools are meant to be run from the command line.

### Code Files

* **CleanMongoData.ipynb**: checks a collection of tweets for duplicates by looking for multiple documents with the same `tweet id` and `user id`
* **MongoTweetGapChecks.ipynb**: checks a collection of tweets for time gaps
* **S3BucketCalcs.ipynb**: calculates statistics of # tweets, storage size and ingest rate from the chunked JSON files in the bucket.
* **MoveS3DataToMongo.py** moves data from a bucket of chunked JSON files into Mongo, checking to make sure the tweet in the JSON file is english and is not already in the MongoDB collection.
* **mongoExtract.py** queries MongoDB for documents and places them in a JSON file in S3. The basic use is to query for english tweets and extract them for placement in S3 storage for processing.


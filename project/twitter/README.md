# Tweet Acquisition Framework
Based on some of the initial tweet acquisition work prepared for Assignment 2, we built out this infrastructure to support storage of data across different media and to accept data from both the search API and the streaming API.

## Explanation of Contents
### Code Files
- **search.py**: Main program used to query the search API for a given search term.  Will gather all available tweets with the search term from the last 7 days (or within a specified subset of dates)
- **track.py**: Our primary program for listening to the twitter firehose via the Streaming API.  Allows for choice of serialization method as appropriate.

### Subdirectories
- **search**: Contains some earlier incarnations of twitter search infrastructure
- **serializers**: Contains several different approaches to serializing tweets to different data storage media, including S3, MongoDB, and (for testing purposes) the console.
- **twitterutils**: Contains supporting files for tweet acquisition, including a framework for storing the required API keys (which aren't included themselves here for security reasons) and a means of effectively restarting the stream in the event of an error.

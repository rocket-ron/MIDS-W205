# Sentiment Analysis Testing Files
This folder contains several pieces of code used for testing, troubleshooting, and tuning our MapReduce jobs.  They are not individually required to generate the final output, but have been instructive examples and useful references, so we have left them in the repository accordingly.

## Explanation of Contents
### Classifiers
- **classify_tweets.py**: Implementation of the sentiment classifier that accepts a trained vectorizer and classifier object and uses it to classify sample tweets from the Mongo instance as either fearful or not.  While these tweets are loaded directly from the mongo instance, they are not scalably streamed in under the MapReduce paradigm, which is why this approach is not used in the final implementation.
- **sentiment_classification.py**: Our first implementation of our sentiment classifier. It is completely self-contained and goes through every step of the process:  extracting tweets from the corpus, training the model, testing the model, querying a sample of new tweets from mongo, and classifying them.  This file was also useful in comparing the performance of the different classification algorithms available in scikit-learn, which is how we came to choose a Linear SVM approach for our final implementation.

### EMR Testing
- **emr_test.py**: This was a trivial job (the output is irrelevant) that was used only to test whether the boostrap actions had successfully installed scikit-learn.
- **get_tweets.py**: Another attempt to stream data from Mongo into Hadoop, but without using the official connector.  Piping the output of this into an MRJob file worked locally, but we found it to be unscalable when run in the cloud.
- **json_test.py**: Tests running a simple MRJob using the JSON input protocol.  This was a prerequisite to our final implementation that pulls JSON data from S3 into MRJob.
- **mongo_test.py**: A simple proof-of-concept implementation of word count to test streaming data directly from Mongo into Hadoop
- **setup_stuff.sh**: An (ultimately abandoned) alternative approach to the bootstrapping process, in which we considered creating a virtualenv python install with all necessary dependencies in place to support the sentiment analysis.  This environment would then be packaged as a tarball and deployed to the EMR cluster during bootstrapping, preventing the need to re-install the dependencies on each node at the start of every job.  Ultimately, we found that this created more problems than it solved and chose to use the slightly slower, but much more robust, method of installing again with each job.

### Supporting Files
- **test.csv**: A sample of 5 tweets from the "Isis" search useful for quick testing

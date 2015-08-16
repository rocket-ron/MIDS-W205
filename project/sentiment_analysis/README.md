# Sentiment Analysis Files
This readme is intended to provide some additional information about the specific code and supporting files used to complete this project.  For a complete explanation of the research context, architecture, and implementation, please see the full report.

## Explanation of Contents
### Code Files
- **fear_count.py**: MapReduce job that identifies fearmongers within our full dataset
- **fear_timeseries.py**: MapReduce job that analyzes changes in the fear response to a given topic over time
- **train_model.py**: Uses a training corpus to generate trained vectorizer and classifier objects that are then saved as pickle files.  These files must be loaded to the EMR cluster before running either of the jobs above

### Supporting Files
- **mrjob.conf**: Configuration file for our EMR clusters.  Defines both cluster specs as well as bootstrap actions
- **tweets-clean.txt**: Corpus of training data for sentiment analyzer containing pre-classified tweets spanning 7 major emotions (including fear).  More details and documentation surrounding the origin of this corpus is availabe [here](http://saifmohammad.com/WebPages/lexicons.html)
- **get-pip.py**: Contains a complete binary for Pip, which we upload as part of the bootstrapping process outline in mrjob.conf.  This self-contained version allows us precise control of exactly what version is used to minimize compatibility problems.
- **mongo-hadoop-bootstrap.sh**: Optional bootstrap step that downloads and installs required supporting files for direct streaming of data from Mongo into Hadoop. Not used presently, but we have saved it here for future iterations.

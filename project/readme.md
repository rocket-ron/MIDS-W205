# Identifying Fearmongers on Twitter - W205 Final Project
## Michael Kennedy, Ron Cordell, Nick Hamlin, Alex Smith

This readme is intended to provide some additional information about the specific code and supporting files used to complete this project.  For a complete explanation of the research context, architecture, and implementation, please see the full report.

The code is organized into four main directories.  Each contains its own readme detailing the contents and execution of the code within that directory.  Other important aspects of the project (like the testing of our sentiment classifier programs) also have their own nested directories and associated explanatory readme files.

## Major Directories (in alphabetical order)
- **dataChecks**: Contains code for validating and cleaning stored data and moving data to different storage media
- **plots**: Code for creating final output visualizations based on results of MapReduce jobs. Also contains .png versions of the created visualizations themselves.
- **sentiment_analysis**: Main directory for all code related to the fear classification of tweets and associated MapReduce jobs.  Contains a subdirectory with all intermediate code used for prototyping and testing as well.
- **tweet_collection**: TODO add tweet code from other repo
- **vagrant**: Contains the necessary setup files to easily spin up our collection infrastructure in a variety of different environments, including EC2 instances, local VMs, and others.

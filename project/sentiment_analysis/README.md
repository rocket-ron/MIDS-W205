#Sentiment Analysis Prototype
Ok, here's how this works

###Installation
Make sure to install scikit-learn first.  If you're using a packed distribution like Anaconda, no action needed.  Otherwise, installation instructions are [here](http://scikit-learn.org/stable/install.html).  In theory, it should be as simple as a `pip install -U numpy scipy scikit-learn` if you're on a mac, which I believe many of us are.

As you can probably tell from the previous paragraph, scikit-learn requires both numpy and scipy, which can be fun adventures to install in their own right.  YMMV, but I've found that using Anaconda makes all of this suck a whole lot less.

###Training Data
`tweets-clean.txt` contains the emotion-tagged corpus of tweets that we're using.  So far, it's the best one I've found, but if anyone comes across anything better, its easy enough to get it.  More info is available [here](http://saifmohammad.com/WebPages/lexicons.html).

###Using the script
This is certainly not the cleanest code in the world, so there will definitely be some refactoring to do when we go to implement this in MapReduce.  In the meantime, the basic process is
- Load tweet corpus and split into training/test data
- Convert both training and test data into sparse matricies of features that will ultimately go into the classifier.  [The blog post](http://marcobonzanini.com/2015/01/19/sentiment-analysis-with-python-and-scikit-learn/) upon which I'm basing this code explains this better.
- Train and test different classification algorithms and compare results. I've commented out the sections of code that do this, and the results are in Table 1 in the Google Doc
- Query some sample data from the mongo server, pass it through the same vectorization process that the training and test data went through, and then pass the result into the winning trained classifier from the previous step.  You can do this for whatever sample of tweets you want, but I chose a selection of the hashtags that we'd gathered that seemed like they'd be obviously fearful or joyful to see if we were even in the right ballpark

# Based on code from:
# https://gist.github.com/bonzanini/c9248a239bbab0e0d42e/download#
# Full discussion:
# https://marcobonzanini.wordpress.com/2015/01/19/sentiment-analysis-with-python-and-scikit-learn


import time
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import sklearn.metrics as m
#from sklearn.externals import joblib


if __name__ == '__main__':
    
    #Build main corpus
    corpus=[]
    with open('tweets-clean.txt','rb') as tsv:
        for line in tsv:
            raw=line.strip().split('\t')
            insert={'id':raw[0][:-1],'text':raw[1],'emotion':raw[2][3:]}
            corpus.append(insert)
    
    def process_tweets (corpus,emotion):
        """extracts tweets from main corpus for a particular emotion"""
        data=[]
        labels=[]
        for tweet in corpus:
            if tweet['emotion']==emotion:
                try:
                    data.append(tweet['text'].decode('utf-8'))
                    labels.append(emotion)
                except UnicodeEncodeError:
                    continue
        return data,labels
    
    #Parse fear/joy tweets out of main corpus, split into train (75%) and test (25%)
    fear_tweets,fear_labels=process_tweets(corpus,'fear')
    joy_tweets,joy_labels=process_tweets(corpus,'joy')
    fear_cutoff=int(len(fear_tweets)*0.75)
    joy_cutoff=int(len(joy_tweets)*0.75)
    train_data = fear_tweets[:fear_cutoff] + joy_tweets[:joy_cutoff]
    train_labels = fear_labels[:fear_cutoff] + joy_labels[:joy_cutoff]
    test_data = fear_tweets[fear_cutoff:] + joy_tweets[joy_cutoff:]
    test_labels = fear_labels[fear_cutoff:] + joy_labels[joy_cutoff:]

    def train_classifier (classifier, train_vectors, train_labels, test_vectors, test_labels):
        """Trains an untrained classifier object based on vectorized training data, 
        then tests for accuracy, precision, and recall based on vectorized test data"""
        t0 = time.time()
        classifier.fit(train_vectors, train_labels)
        t1 = time.time()
        prediction=classifier.predict(test_vectors)
        t2 = time.time()
        time_train=t1-t0
        time_predict=t2-t1
        accuracy=m.accuracy_score(test_labels,prediction)
        #fear is hardcoded in the next two lines...heads up
        precision=m.precision_score(test_labels,prediction,pos_label='fear',average='micro')
        recall=m.recall_score(test_labels,prediction,pos_label='fear',average='micro')
        print("Training Results for "+str(type(classifier).__name__))
        print("Training time: %fs; Prediction time: %fs" % (time_train, time_predict))
        print("Accuracy: {0}, Precision: {1}, Recall:{2}".format(str(accuracy),str(precision),str(recall)))
        return classifier
        # Create feature vectors
    vectorizer = TfidfVectorizer(min_df=5,max_df = 0.8,sublinear_tf=True,use_idf=True)
    train_vectors = vectorizer.fit_transform(train_data)
    test_vectors = vectorizer.transform(test_data)
     
    
    # Perform classification with SVM, kernel=linear
    classifier_liblinear = svm.LinearSVC()
    trained_liblinear_classifier=train_classifier(classifier_liblinear,train_vectors, train_labels, test_vectors, test_labels)
    #joblib.dump(trained_liblinear_classifier, 'class.pkl', compress=9)   
    with open( "classifier.pkl", "wb" ) as f:
        pickle.dump(trained_liblinear_classifier,f)
    with open( "vectorizer.pkl", "wb" ) as v:
        pickle.dump(vectorizer,v)

# Based on code from:
# https://gist.github.com/bonzanini/c9248a239bbab0e0d42e/download#
# Full discussion:
# https://marcobonzanini.wordpress.com/2015/01/19/sentiment-analysis-with-python-and-scikit-learn


import time
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.linear_model import LogisticRegression
import sklearn.metrics as m

import pymongo

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

    # Create feature vectors
    vectorizer = TfidfVectorizer(min_df=5,
                                 max_df = 0.8,
                                 sublinear_tf=True,
                                 use_idf=True)
    train_vectors = vectorizer.fit_transform(train_data)
    test_vectors = vectorizer.transform(test_data)

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
    
    def predict (trained_classifier, test_vectors):
        """Accepts a trained classifer object and a set of test tweets. 
        Make sure they're vectorized properly first!"""
        t0 = time.time()
        prediction=trained_classifier.predict(test_vectors)
        t1 = time.time()
        time_predict=t1-t0
        print("Prediction Results for "+str(type(trained_classifier).__name__))
        print("Prediction time: %fs" % (time_predict))
        return prediction
        
#    # Perform classification with SVM, kernel=rbf
#    classifier_rbf = svm.SVC()
#    trained_rbf_classifier=train_classifier(classifier_rbf,train_vectors, train_labels, test_vectors, test_labels)
#
#    # Perform classification with SVM, kernel=linear
#    classifier_linear = svm.SVC(kernel='linear')
#    trained_linear_classifier=train_classifier(classifier_linear,train_vectors, train_labels, test_vectors, test_labels)

    # Perform classification with SVM, kernel=linear
    classifier_liblinear = svm.LinearSVC()
    trained_liblinear_classifier=train_classifier(classifier_liblinear,train_vectors, train_labels, test_vectors, test_labels)
    
#    # Perform Classification with Logistic Regression
#    classifier_logit = LogisticRegression()
#    trained_logit_classifier=train_classifier(classifier_logit,train_vectors, train_labels, test_vectors, test_labels)
    
    def predict_from_mongo(term,count,trained_classifier):
        """Extract a sample of tweets from remote mongo instance and predict 
        via a previously trained classifier object"""
        t0 = time.time()
        conn=pymongo.MongoClient(host='54.153.43.230',port=27017)
        tweets = conn['twitter_db'][term]
        predict_tweets=list(tweets.find().limit(count))
        t1 = time.time()
        #Make sure to vectorize new data using the same process as the training data!
        predict_data=[i['text'] for i in predict_tweets]
        predict_vectors = vectorizer.transform(predict_data)
        predicted_emotions=predict(trained_classifier,predict_vectors)
        t2 = time.time()
        time_query=t1-t0
        time_process=t2-t0
        results=Counter(predicted_emotions)
        print "Results for {1} tweets about {0}: {2}".format(term,count,results.items())
        print("Query time: %fs; Total processing time: %fs" % (time_query, time_process)) 
        return zip(predict_data,predicted_emotions)
        
    output_isis=predict_from_mongo('isis',500,trained_liblinear_classifier)
    output_july=predict_from_mongo('july4',500,trained_liblinear_classifier)
    output_worldcup=predict_from_mongo('worldcup',500,trained_liblinear_classifier)
    output_immigration=predict_from_mongo('immigration',500,trained_liblinear_classifier)

    

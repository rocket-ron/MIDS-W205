# Based on code from:
# https://gist.github.com/bonzanini/c9248a239bbab0e0d42e/download#
# Full discussion:
# https://marcobonzanini.wordpress.com/2015/01/19/sentiment-analysis-with-python-and-scikit-learn

#http://stackoverflow.com/questions/25788151/bringing-a-classifier-to-production
#http://blog.scrapinghub.com/2014/03/26/optimizing-memory-usage-of-scikit-learn-models-using-succinct-tries/

import time
from collections import Counter
import pickle

import pymongo

if __name__ == '__main__':
      
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
        
    def predict_from_mongo(term,count,trained_classifier,vectorizer):
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
    
    with open("classifier.pkl","rb") as f:
        trained_liblinear_classifier=pickle.load(f)
    with open("vectorizer.pkl","rb") as v:
        vectorizer=pickle.load(v)
   
    #trained_liblinear_classifier = joblib.load('class.pkl')    
    output_isis=predict_from_mongo('isis',500,trained_liblinear_classifier,vectorizer)
#    output_july=predict_from_mongo('july4',500,trained_liblinear_classifier)
#    output_worldcup=predict_from_mongo('worldcup',500,trained_liblinear_classifier)
#    output_immigration=predict_from_mongo('immigration',500,trained_liblinear_classifier)

    

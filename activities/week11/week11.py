# Pick 10 words from the 1789-Washington.txt. Calculate the tf-idf score for those 10 words.
from math import log
import glob

# files = ['1789-Washington.txt','1797-Adams.txt','1801-Jefferson.txt']

q_terms=['citizens','supplication','executive','despondence','veneration','tranquility','palliated','vicissitudes','it','to']

def tf(term, doc):
	doc = doc.lower().split()
	return doc.count(term.lower()) / float(len(doc))

def idf(term, corpus):
	num_doc_with_term=0
	for text in corpus:
		if term.lower() in text.lower().split():
			num_doc_with_term += 1
	if num_doc_with_term == 0:
		return 0.0
	else:
		return 1.0 + log(float(len(corpus))/num_doc_with_term)

def tf_idf(term, doc, corpus):
	return tf(term, doc) * idf(term, corpus)

corpus = []
files = glob.glob('inaugural/*.txt')
for f in files:
	with open(f) as d:
		corpus.append(d.read())

doc_result = []
for doc in corpus:
	term_result = {}
	for term in q_terms:
		term_result[term] = tf_idf(term, doc, corpus)
	doc_result.append(term_result)

for result in doc_result:
	print result


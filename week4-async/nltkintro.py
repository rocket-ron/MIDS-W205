import nltk
from pprint import pprint

def demo_zipflaw():
	from nltk.book import text4
	fd = nltk.FreqDist([w.lower() for w in text4[:1000] if w.isalpha()])
	fd.plot(50)
	pprint(fd.items())


if __name__ == '__main__':
	demo_zipflaw()


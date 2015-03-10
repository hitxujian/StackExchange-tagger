import sys
import os
import json
import time
import string

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if not path in sys.path:
    sys.path.insert(1, path)
del path

try:
    import database.mongo as mongo
except ImportError as exc:
    print("Error: failed to import settings module ({})".format(exc))

try:
    import nltk
except ImportError as exc:
    print("Error: failed to import settings module ({})".format(exc))

try:
	from bs4 import BeautifulSoup
except ImportError as exc:
	print("Error: failed to import settings module ({})".format(exc))

test_data = "data/processed.csv"
stopword_data = "data/stopword.txt"
replaceword_data = "data/replaceword.txt"

def preprocess_dataset():
	count = 0
	with open(test_data) as infile:
		for line in infile:
			if(line[-3:]=="\"\r\n"):
				#End of one post
				print line.strip()
			else:
				print line.strip(),
			count+=1
	# print count

def remove_stopwords():

	porter_stemmer = nltk.stem.porter.PorterStemmer()
	wordnet_lemmatizer = nltk.stem.WordNetLemmatizer()
	nltk_stopwords = nltk.corpus.stopwords.words('english')
	
	stopwords = {}
	replace_words = {}
	stopword_count = 0
	takenword_count = 0

	with open(stopword_data) as infile:
		for line in infile:
			i = line.strip().split()
			for token in i:
				a = wordnet_lemmatizer.lemmatize(porter_stemmer.stem(token))
				if a not in stopwords:
					stopwords[a] = 1

	for token in nltk_stopwords:
		a = wordnet_lemmatizer.lemmatize(porter_stemmer.stem(token))
		if a not in stopwords:
			stopwords[a] = 1

	for a in string.punctuation:
		if a not in replace_words:
			replace_words[a] = 1
	
	with open(replaceword_data) as infile:

		for line in infile:
			a = line.strip()
			if a not in replace_words:
				replace_words[a] = 1			

	with open(test_data) as infile:
		for line in infile:
			striped_line = line.strip()
			if striped_line :
				a = striped_line.split(',',2)
				post_id = str(a[0])
				title = str(a[1])
				a = a[2].rsplit(',',1)
				tag_list_string = a[1]
				body = a[0]
				#print body  
				soup = BeautifulSoup(body)
				body = soup.get_text()
				for i in replace_words:
					body = body.replace(i, ' ')
				list_token = nltk.word_tokenize(body)
				for token in list_token:
					processed_token = wordnet_lemmatizer.lemmatize(porter_stemmer.stem(token.strip().lower()))
					if(processed_token in stopwords):
						stopword_count+=1
					else:
						takenword_count+=1
						print processed_token
			print "\n"
	print "stopword_count : ", stopword_count
	print "takenword_count : ", takenword_count	
#preprocess_dataset()
remove_stopwords()

# -*- coding: utf-8 -*-
"""
Created on Tue May 28 17:52:16 2019

@author: taina.esteves
"""

# import statements
import pickle
#from sklearn.cluster import KMeans
#from sklearn import metrics
#from sklearn.feature_extraction import text
#from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
import sys

stemmer = SnowballStemmer('english')
tokenizer = RegexpTokenizer(r'[a-zA-Z\']+')

def tokenize(text):
    '''  s.lower() é um método que retorna a lowercased version of the string text:
        função tokenize recebe texto em desc, gera tokens a partir da divisão as strings em substrings (palavras), e reduzem as mesmas a sua raíz'''
    return [stemmer.stem(word) for word in tokenizer.tokenize(text.lower())]

with open('lib/finalized_clustering_model.sav', 'rb') as fid:
    model = pickle.load(fid)

with open('lib/finalized_vectorizer_model.sav', 'rb') as fid:
    vectorizer = pickle.load(fid)
    

def cluster_predict(str_input):    
    Y = vectorizer.transform([str_input])
    prediction = model.predict(Y)
    return prediction
    
if __name__ == '__main__':
    a = sys.argv[1]
    print(cluster_predict(a)[0])
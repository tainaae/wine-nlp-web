# coding: utf-8
# utilizando análises feitas por @kitakoj (https://github.com/kitakoj18/wine_descp) and @zackthoutt (https://github.com/zackthoutt/wine-deep-learning) 



from sqlalchemy import create_engine
#NPL 
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
#CLUSTERING
import pandas as pd 
#import matplotlib.pyplot as plt
#import seaborn as sns
from sklearn.cluster import KMeans
import pickle
#from sklearn import metrics
#normalização
from sklearn import preprocessing
import numpy as np
#from recommendation import Recommendation

#dados da tabela variety_df do banco de dados mysql para dataframe
######################################################
host='127.0.0.1' 
user='****' 
password='********'
db='wine'

engine = create_engine('mysql+pymysql://' + user + ':' + password + '@' + host + '/' + db)


variety_df = pd.read_sql_table('variety_df', con=engine, schema=None, index_col=None, coerce_float=False, parse_dates=None, columns=None, chunksize=None)
#variety_df = pd.read_csv('variety_df.csv', sep=',')

#NPL
######################################################
listadd_stopwords = ["attract","flavor", "alongside", "bring", "drink", "feel", "like", "month", 
                     "note", "offer", "abov", "afterward", "alon", "alongsid", "alreadi", "alway", 
                     "ani", "anoth", "anyon", "anyth", "anywher", "becam", "becaus", "becom", "befor", 
                     "besid", "cri", "describ", "dure", "els", "elsewher", "empti", "everi", "everyon", 
                     "everyth", "everywher", "fifti", "forti", "henc", "hereaft", "herebi", "howev", 
                     "hundr", "inde", "mani", "meanwhil", "moreov", "nobodi", "noon", "noth", 
                     "nowher", "onc", "onli", "otherwis", "ourselv", "perhap", "pleas", "sever", "sinc", 
                     "sincer", "sixti", "someon", "someth", "sometim", "somewher", "themselv", "thenc", 
                     "thereaft", "therebi", "therefor", "togeth", "twelv", "twenti", "veri", "whatev", 
                     "whenc", "whenev", "wherea", "whereaft", "wherebi", "wherev", "whi", "yourselv", "anywh", 
                     "el", "elsewh", "everywh", "ind", "otherwi", "plea", "somewh", "attract", "bring", 
                     "american", "french", "bottl", "year", "aftertast", "aroma", "bright", "charact", 
                     "crush", "follow", "lead", "nose", "readi", "tast", "wine", "color", "dre", "palat"
                     "vineyard", "ferment", "finish", "mourv", "open", "good", "singl", "sourc", "design", 
                     "come", "whiff", "zin"]

punc = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',"%"]
'''define stop_words como a junção de qualquer dos 
elementos do dicionário ENGLISH_STOP_WORDS com qualquer pontuação'''
stop_words = text.ENGLISH_STOP_WORDS.union(punc, listadd_stopwords)

''' stemmers reduzem palavras à suas respectivas raízes
Create a new instance of a language specific subclass
'''
stemmer = SnowballStemmer('english')

'''A RegexpTokenizer splits a string into substrings using a regular expression.'''
tokenizer = RegexpTokenizer(r'[a-zA-Z\']+')

def tokenize(text):
    '''  s.lower() é um método que retorna a lowercased version of the string text:
        função tokenize recebe texto em desc, gera tokens a partir da divisão as strings em substrings (palavras), e reduzem as mesmas a sua raíz'''
    return [stemmer.stem(word) for word in tokenizer.tokenize(text.lower())]

#array que recebe os valores da coluna description de variety_df
desc = variety_df['description'].values

'''vetorizer é o objeto que faz a vetorizaçao de palavras no caso abaixo, o vetor das stop words é removido e é gerado um vetor sem as mesmas contendo só as palavras que podem ter alguma informacao relevante'''
vectorizer = TfidfVectorizer(stop_words = stop_words, tokenizer = tokenize, max_features = 1000)

X = vectorizer.fit_transform(desc)
words = vectorizer.get_feature_names()

filename = 'finalized_vectorizer_model.sav'
pickle.dump(vectorizer, open(filename, 'wb'))

#CLUSTERING
######################################################

kmeans = KMeans(n_clusters = 20, n_init = 10, n_jobs = -1)

''' Computa o cluster com os paramentros especificado em kmeans nos dados de X  '''
kmeans.fit(X)


''' common_words é uma matriz que relaciona clusters com a posição da palavra na lista words '''
common_words = kmeans.cluster_centers_.argsort()[:,-1:-11:-1]
info_clusters = pd.DataFrame(columns=['w0','w1','w2','w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9'])

for num, centroid in enumerate(common_words):
  info_clusters.loc[num, ['w0']] = words[centroid[0]]  
  info_clusters.loc[num, ['w1']] = words[centroid[1]]
  info_clusters.loc[num, ['w2']] = words[centroid[2]]
  info_clusters.loc[num, ['w3']] = words[centroid[3]]
  info_clusters.loc[num, ['w4']] = words[centroid[4]]
  info_clusters.loc[num, ['w5']] = words[centroid[5]]
  info_clusters.loc[num, ['w6']] = words[centroid[6]]
  info_clusters.loc[num, ['w7']] = words[centroid[7]]
  info_clusters.loc[num, ['w8']] = words[centroid[8]]
  info_clusters.loc[num, ['w9']] = words[centroid[9]]

''' com base no '''
variety_df['cluster'] = kmeans.labels_

''' série clusters TALVEZ deva ser mandada para banco de dados'''
clusters = variety_df.groupby(['cluster', 'variety', 'country']).size()

'''exporta modelo kmeans criado para o arquivo com o nome indicado'''
filename = 'finalized_clustering_model.sav'
pickle.dump(kmeans, open(filename, 'wb'))

#classify wines of table variety_df
######################################################
variety_df['ClusterPrediction'] = ""
# load model and previous preprocessing - load model only once
with open('finalized_clustering_model.sav', 'rb') as fid:
    model = pickle.load(fid)

#geração de dataframe com a pontuação de cada cluster 
#associado aos tipos de uva e país
######################################################
clusters_df = pd.Series.to_frame(clusters)
clusters_df['column'] = list(clusters.index)
clusters_df['cluster'], clusters_df['variety'], clusters_df['country'] = clusters_df.column.str[0], clusters_df.column.str[1], clusters_df.column.str[2]
clusters_df = clusters_df.drop(columns='column')
clusters_df = clusters_df.rename(columns={0: 'points'})

#Transpoe indexes and columns
info_clusters = info_clusters.T
#transforma as palavras relacionadas a cada cluster em dicionario para comparar com a entrada dos usuários
clusters_dictionary = info_clusters.to_dict(orient = 'list')

def cluster_predict(str_input):
    Y = vectorizer.transform([str_input])
    prediction = model.predict(Y)
    return prediction

# Cluster category for each variety
variety_df['ClusterPrediction']=variety_df.apply(lambda x: cluster_predict(x[2]), axis=1)

#normalização dos dados
#x_array = np.array(clusters_df['points'])
#normalized_X = preprocessing.normalize([x_array])
#normalized_X = normalized_X.T
#clusters_df['points'] = normalized_X*1000

varieties = variety_df['variety'].value_counts().index.tolist()
countries = variety_df['country'].value_counts().index.tolist()

info_clusters.to_sql(name='info_clusters', con=engine, if_exists = 'replace', index=False)
clusters_df.to_sql(name='clusters_df', con=engine, if_exists = 'replace', index=False)

# -*- coding: utf-8 -*-

import pymongo
import nltk
import re
import pip as csv
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_predict

    #ler e contar arqivo de 8900 tweets para treinamento
dataset = pd.read_csv('Tweets_Mg.csv',encoding='utf-8')
dataset.count()
    #separar tweets das classes
tweets = dataset['Text'].values
classes = dataset['Classificacao'].values
    #treinamento de modelo do tipo Naive Bayes Multinomial
vectorizer = CountVectorizer(ngram_range=(1,2))
freq_tweets = vectorizer.fit_transform(tweets)
modelo = MultinomialNB()
modelo.fit(freq_tweets,classes)
    # conexão com banco
conn = pymongo.MongoClient()
db = conn['Congresso']
coll = db['Tweets']
lista = coll.find()
    #analise dos tweets do banco com modelo treinado e impressão do sentimento
for list in lista:
    print list['Post'][0]['Tweet']
    testes = [list['Post'][0]['Tweet']]
    freq_testes = vectorizer.transform(testes)
    print modelo.predict(freq_testes)



resultados = cross_val_predict(modelo, freq_tweets, classes, cv=10)
print ('Acuracia:')
print metrics.accuracy_score(classes,resultados)

sentimento=['Positivo','Negativo','Neutro']
print (metrics.classification_report(classes,resultados,sentimento))

print (pd.crosstab(classes, resultados, rownames=['Real'], colnames=['Predito'], margins=True))
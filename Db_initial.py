import pymongo
from pymongo import MongoClient
import csv

#Script inicia banco de dados no mongo
#faz o Insert de todos os politicos lendo de 4 arquivos csv

try:
    conn = MongoClient('localhost', 27017)
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e
conn

db = conn['Congresso']

quer = ['Senador', 'Dep_Federal', 'Dep_Estadual', 'Vereador']
for query in quer:
    doc = query + '.csv'
    cr = csv.reader(open(doc, "rb"), delimiter=';')
    coll = db[query]
    i = 0
    for read in cr:
        print(read)
        obj = [{"Congressista": { "Nome":  read[4], "Nome Civil":  read[3], "Partido":  read[1], "Estado": read[0], "id": '', "Cargo": read[5]},},]

        coll.insert(obj)

        print 'insert'
        print i
        i = i + 1
    print()
    print query
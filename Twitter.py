import pymongo
import json
import oauth2
import time
import re

def Processador(text):
    result = re.sub(r"http\S+", "", text)
    result= re.sub('[!@#$]','', result)
    return result

def Search(quest):
    consumer_Key = 'XELDltS01IxUMQDMDlTP5Tax5'
    consumer_Secret = 'z6rGY8x1ZQ4g7Jhre9OrF9O3t5P0yFs8iRqaaPDgG0ioxtVev8'

    token_key = '4238064022-OKb4QxPDCtalC26R3D39SZoJhBcsixrhozKJIvm'
    token_Secret = 'ELqC5lBvrgyUFWRVwVU4wA09bSL6isx9DcFrTTqwbWwTp'

    consumer = oauth2.Consumer(consumer_Key, consumer_Secret)
    token = oauth2.Token(token_key, token_Secret)

    cliente = oauth2.Client(consumer, token)

    requisicao = cliente.request('https://api.twitter.com/1.1/search/tweets.json?q=' + quest + '&lang= pt&count=100$sleep_on_rate_limit=True')

    Dcode = requisicao[1].decode()
    objeto = json.loads(Dcode)
    return objeto


conn = pymongo.MongoClient()
db = conn['Congresso']

quer = ['Senador', 'Dep_Estadual', 'Dep_Federal', 'Vereador']

for query in quer:
    coll = db[query]
    cou = db['Tweets']

    reads = coll.find()
    i= x = 0
    for read in reads:

        cargo = read['Congressista']['Cargo']
        nome = read['Congressista']['Nome']
        id = read['_id']
        quest = cargo + ' ' + nome
        print ("Politico: %s" % (i+1))

        result = Search(quest)
        i = i + 1
        try:

         for tweet in result.get('statuses', None):
            twet = tweet.get('user', None)

            Ninter = twet.get('scream_name', None)
            text = tweet.get('text', None)
            id_str = tweet.get('id_str', None)


            text = Processador(text)
            print text

            post = {
                'Post': [{"Internauta": Ninter, "Tweet": text, "Id_str": id_str}, {'id_origem': id}]}

            cou.insert(post)
            print post
        except:
            if result.get('statuses', None) == None:
                x = x+1
                print("Erro: %s, %s" % (x, time.strftime("%H:%M,%S", time.gmtime())))
                time.sleep(60 * 15)
                print("Continue : %s" % (time.strftime("%H:%M,%S", time.gmtime())))
                continue

# print(coll)



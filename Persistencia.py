import json
from Consola import Candidato
import os

def cargar():
    dicc = {}
    for candidato in [e.value for e in Candidato]:
        dicc[candidato] = {}
        file = open(os.getcwd() + '\\' + str(candidato).replace('@', '').lower() + '.j', 'r')
        lista = json.load(file)
        for tweet in lista:
            dicc[candidato][tweet['id']] = tweet
        file.close()
    return dicc

def guardar(dicc):
    for candidato, tweets in dicc.items():
        file = open(os.getcwd() + '\\' + str(candidato).replace('@', '').lower() + '.j', 'w')
        lista = []
        for tweet in tweets.values():
            lista.append(tweet)
        json.dump(lista, file)
        file.close()
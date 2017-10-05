import json
from Consola import Candidato

def cargar():
    dicc = {}
    for candidato in [e.value for e in Candidato]:
        dicc[candidato] = json.load(open(str(candidato).replace('@', '').lower() + '.json', 'r'))
    return dicc

def guardar(dicc):
    for candidato, tweets in dicc.items():
        tweets_olds = []
        #with open(str(candidato).replace('C:\\Untref\\TP2Estruc' + '@', '').lower() + '.txt', 'r') as file:
        #    tweets_olds = json.load(file)
        tweets_olds += tweets
        with open(open(str(candidato).replace('@', '').lower() + '.j', 'w')) as file:
            json.dump(tweets_olds, file)
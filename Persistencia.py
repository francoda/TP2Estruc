import json
from Consola import Candidato
import os

def cargar():
    dicc = {e.value:{} for e in Candidato}
    for candidato in [e.value for e in Candidato]:
        try:
            file = open(os.getcwd() + '\\' + str(candidato).replace('@', '').lower() + '.j', 'r')
            lista = json.load(file)
            for tweet in lista:
                dicc[candidato][tweet['id']] = tweet
            file.close()
        except FileNotFoundError:
            dicc[candidato] = {}
    return dicc

def guardar(dicc):
    for candidato, tweets in dicc.items():
        file = open(os.getcwd() + '\\' + str(candidato).replace('@', '').lower() + '.j', 'w')
        lista = []
        for tweet in tweets.values():
            lista.append(tweet)
        json.dump(lista, file)
        file.close()

def cargarEstadisticas():
    try:
        last_id = 0
        fist_id = 0
        file = open(os.getcwd() + '\\Estadisticas.txt', 'r')
        for line in file.readlines():
            if 'last_id' in line:
                last_id = int(line.split(":",1)[1])
            elif 'fist_id' in line:
                fist_id = int(line.split(":",1)[1])
        file.close()
        return last_id, fist_id
    except FileNotFoundError:
        return 0, 0

def guardarEstadisticas(resumen):
    file = open(os.getcwd() + '\\Estadisticas.txt', 'w')
    file.writelines(resumen)
    file.close()
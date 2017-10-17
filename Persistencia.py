import json
from Consola import Candidato
from Estadisticas import quitar_acentos
import os
import csv
import re

def cargar():
    dicc = {e.value:{} for e in Candidato}
    for candidato in [e.value for e in Candidato]:
        try:
            file = open(os.getcwd() + '\\Base\\' + str(candidato).replace('@', '').lower() + '.j', 'r')
            lista = json.load(file)
            for tweet in lista:
                dicc[candidato][tweet['Id']] = tweet
            file.close()
        except FileNotFoundError:
            dicc[candidato] = {}
    return dicc

def guardar(dicc):
    for candidato, tweets in dicc.items():
        file = open(os.getcwd() + '\\Base\\' + str(candidato).replace('@', '').lower() + '.j', 'w')
        lista = []
        for tweet in tweets.values():
            lista.append(tweet)
        json.dump(lista, file)
        file.close()

def cargarEstadisticas():
    try:
        last_id = 0
        fist_id = 0
        file = open(os.getcwd() + '\\Base\\Estadisticas.txt', 'r')
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
    file = open(os.getcwd() + '\\Base\\Estadisticas.txt', 'w')
    file.writelines(resumen)
    file.close()

def generar_diccionario_afectos():
    diccionario_afectos = {}
    file = open('Documentacion\\Diccionario_Afectos.csv', 'r')
    reader = csv.reader(file, delimiter=';')

    for renglon in reader:
        if renglon[0][len(renglon[0]) - 1] != 'N':
            palabra = re.sub(r'(\_\w)?', '', renglon[0]) #Usa una expresión regular para identificar las palabras que finalicen con "_ + una letra cualquiera" y lo reemplaza por nada, es decir, lo corta.
            palabra = quitar_acentos(palabra)
            puntaje = float(renglon[1])
            #puntaje = re.sub(r'[\.]', '', renglon[1])
            diccionario_afectos[palabra] = float(puntaje) #int(puntaje) #Genera un diccionario cuya clave es una palabra normalizada y su valor representa el "score" de dicha palabra.

    return diccionario_afectos

def cargar_STOP_WORDS():
    try:
        STOP_WORDS = []
        file = open(os.getcwd() + '\\Documentacion\\STOP_WORDS.txt', 'r')
        for line in file.readlines():
            line = quitar_acentos(line)
            STOP_WORDS.append(line)
        file.close()
        return STOP_WORDS
    except FileNotFoundError:
        return ['URL','USER']

import json
import os
import re

STOP_WORDS = ['URL','USER']

def leer_tweets():
    from Consola import Candidato #Nose por qué no funciona si lo pongo arriba con el resto de los import
    apariciones_palabras = {e.value: {} for e in Candidato}
    for candidato in [e.value for e in Candidato]:
        try:
            file = open(os.getcwd() + '\\Base\\' + str(candidato).replace('@', '').lower() + '.j', 'r')
            lista = json.load(file)
            for tweet in lista:
                texto = limpiar_texto(tweet['Texto'])
                palabras = re.split(r'[\s]+', texto)
                for p in palabras:
                    if len(p) >= 3 and p not in STOP_WORDS:
                        if p not in apariciones_palabras[candidato].keys():
                            apariciones_palabras[candidato][p] = 1
                        else:
                            apariciones_palabras[candidato][p] += 1
            file.close()
            print(candidato + ':')
            print(apariciones_palabras[candidato])
        except FileNotFoundError:
            apariciones_palabras[candidato] = {}
    return apariciones_palabras

def limpiar_texto(texto):
    texto = re.sub(r'([A-Z]+)', lambda match: r'{}'.format(match.group(1).lower()), texto) #Paso a minúsculas
    texto = re.sub(r'[^a-z@áéíóú\s]', '', texto) #Borro caracteres especiales
    texto = re.sub(r'\B@[\S]+', 'USER', texto) #Borro usuarios
    #Saco acentos
    texto = re.sub(r'[á]', 'a', texto)
    texto = re.sub(r'[é]', 'e', texto)
    texto = re.sub(r'[í]', 'i', texto)
    texto = re.sub(r'[ó]', 'o', texto)
    texto = re.sub(r'[ú]', 'u', texto)
    texto = re.sub(r'[\S]*(http)[\S]+', 'URL', texto) #Borro links (si están pegados a una palabra a su izquierda también)
    texto = re.sub(r'[\S]+@[\S]+', 'URL', texto) #Borro emails
    return texto


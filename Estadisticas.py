import json
import os
import re
import Persistencia
from Modelos import *

def leer_tweets():
    STOP_WORDS = Persistencia.cargar_STOP_WORDS()
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
            #print(candidato + ':')
            #print(apariciones_palabras[candidato])
        except FileNotFoundError:
            apariciones_palabras[candidato] = {}
    return apariciones_palabras

def limpiar_texto(texto):
    texto = re.sub(r'([A-Z]+)', lambda match: r'{}'.format(match.group(1).lower()), texto) #Paso a minúsculas
    texto = re.sub(r'[^a-z@áéíóú\s]', '', texto) #Borro caracteres especiales
    texto = re.sub(r'\B@[\S]+', 'USER', texto) #Borro usuarios
    #Saco acentos
    texto = Persistencia.quitar_acentos(texto)
    texto = re.sub(r'[\S]*(http)[\S]+', 'URL', texto) #Borro links (si están pegados a una palabra a su izquierda también)
    texto = re.sub(r'[\S]+@[\S]+', 'URL', texto) #Borro emails
    return texto

def puntuar_tweets(apariciones_palabras = {}):
    diccionario_afectos = Persistencia.generar_diccionario_afectos()
    diccionario_puntajes = {}

    for candidato, palabras in apariciones_palabras.items(): #Para cada candidato y cada palabra asociada al mismo
        puntaje_candidato = 0
        for palabra, cantidad in palabras.items():
            if palabra in diccionario_afectos.keys():
                puntaje_candidato += diccionario_afectos[palabra]*cantidad
        diccionario_puntajes[candidato] = puntaje_candidato
            #Se puede agregar un else que guarde aquellas palabras que no aparecieron en el diccionario de afectos, de manera de mantener un control interno.
    #print('Puntajes:')
    #print(diccionario_puntajes)
    return diccionario_puntajes

def quitar_acentos(texto):
    texto = re.sub(r'[á]', 'a', texto)
    texto = re.sub(r'[é]', 'e', texto)
    texto = re.sub(r'[í]', 'i', texto)
    texto = re.sub(r'[ó]', 'o', texto)
    texto = re.sub(r'[ú]', 'u', texto)
    return texto
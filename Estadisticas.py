import json
import os
import re

def leer_tweets():
    from Consola import Candidato #Nose por qué no funciona si lo pongo arriba con el resto de los import
    apariciones_palabras = {e.value: {} for e in Candidato}
    for candidato in [e.value for e in Candidato]:
        try:
            file = open(os.getcwd() + '\\Base\\' + str(candidato).replace('@', '').lower() + '.j', 'r')
            lista = json.load(file)
            for tweet in lista:
                texto = tweet['Texto'].lower() #En teoría no hay que usar esto y hay que hacer el lower con regulares (preguntar)
                texto = limpiar_texto(texto)
                palabras = re.split(r'[\s]+', texto)
                if '' in palabras:
                    palabras.remove('')
                for p in palabras:
                    if len(p) >= 3:
                        if p not in apariciones_palabras[candidato].keys():
                            apariciones_palabras[candidato][p] = 1
                        else:
                            apariciones_palabras[candidato][p] += 1
            file.close()
        except FileNotFoundError:
            apariciones_palabras[candidato] = {}
    print(apariciones_palabras)
    return apariciones_palabras

def limpiar_texto(texto):
    texto = texto = re.sub(r'[^a-z@áéíóú\s]', '', texto) #Borro caracteres especiales
    texto = re.sub(r'\B@[\S]+', 'USER', texto) #Borro usuarios
    #Saco acentos
    texto = re.sub(r'[á]', 'a', texto)
    texto = re.sub(r'[é]', 'e', texto)
    texto = re.sub(r'[í]', 'i', texto)
    texto = re.sub(r'[ó]', 'o', texto)
    texto = re.sub(r'[ú]', 'u', texto)
    texto = re.sub(r'(http)[\S]+', 'URL', texto) #Borro links
    texto = re.sub(r'[\S]+@[\S]+', 'URL', texto) #Borro emails
    return texto
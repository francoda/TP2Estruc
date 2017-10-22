import json, os, re
import Persistencia
from Modelos import *
from nltk.stem.snowball import SnowballStemmer

sbEsp = SnowballStemmer('spanish')
LONGITUD_MINIMA = 3

def cantidad_tweets():
    listaCantidad = []
    for candidato, tweets in Persistencia.cargar().items():
        listaCantidad.append((candidato, len(tweets)))
    return sorted(listaCantidad, key=lambda tup: tup[1], reverse=True)

def puntuar_tweets():
    apariciones_palabras = leer_tweets()
    diccionario_afectos = Persistencia.generar_diccionario_afectos()
    diccionario_puntajes = []

    for candidato, palabras in apariciones_palabras.items(): #Para cada candidato y cada palabra asociada al mismo
        puntaje_candidato = 0
        cantidad_palabras_puntaje = 0
        for palabra, cantidad in palabras.items():
            if palabra in diccionario_afectos.keys():
                puntaje_candidato += diccionario_afectos[palabra]*cantidad
                cantidad_palabras_puntaje += cantidad
        if cantidad_palabras_puntaje > 0:
            diccionario_puntajes.append((candidato,puntaje_candidato/cantidad_palabras_puntaje))
        else:
            diccionario_puntajes.append((candidato, 0))
    return sorted(diccionario_puntajes, key=lambda tup: tup[1], reverse=True)

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
                    if len(p) >= LONGITUD_MINIMA:
                        p = sbEsp.stem(p)
                        if p not in STOP_WORDS:
                            if p not in apariciones_palabras[candidato].keys():
                                apariciones_palabras[candidato][p] = 1
                            else:
                                apariciones_palabras[candidato][p] += 1
            file.close()
        except FileNotFoundError:
            apariciones_palabras[candidato] = {}
    return apariciones_palabras

def limpiar_texto(texto):
    texto = re.sub(r'([A-Z]+)', lambda match: r'{}'.format(match.group(1).lower()), texto) #Paso a minúsculas
    texto = re.sub(r'[^a-z@áéíóú\s]', '', texto) #Borro caracteres especiales
    texto = re.sub(r'\B@[\S]+', 'USER', texto) #Borro usuarios
    texto = re.sub(r'[á]', 'a', texto) #Quitar acentos
    texto = re.sub(r'[é]', 'e', texto)
    texto = re.sub(r'[í]', 'i', texto)
    texto = re.sub(r'[ó]', 'o', texto)
    texto = re.sub(r'[ú]', 'u', texto)
    texto = re.sub(r'[\S]*(http)[\S]+', 'URL', texto) #Borro links (si están pegados a una palabra a su izquierda también)
    texto = re.sub(r'[\S]+@[\S]+', 'URL', texto) #Borro emails
    return texto

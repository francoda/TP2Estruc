import json, os, csv, re
from Consola import Candidato
from nltk.stem.snowball import SnowballStemmer

sbEsp = SnowballStemmer('spanish')

def cargar():
    dicc = {e.value:{} for e in Candidato}
    if not os.path.exists(os.getcwd() + '\\Base\\'):
        os.makedirs(os.getcwd() + '\\Base\\')
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
    if not os.path.exists(os.getcwd() + '\\Base\\'):
        os.makedirs(os.getcwd() + '\\Base\\')
    for candidato, tweets in dicc.items():
        file = open(os.getcwd() + '\\Base\\' + str(candidato).replace('@', '').lower() + '.j', 'w')
        lista = []
        for tweet in tweets.values():
            lista.append(tweet)
        json.dump(lista, file)
        file.close()

def eliminarBase():
    for root, dirs, files in os.walk(os.getcwd() + '\\Base\\', topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def cargarBusquedaLog():
    try:
        last_id = 0
        fist_id = 0
        if not os.path.exists(os.getcwd() + '\\Base\\'):
            os.makedirs(os.getcwd() + '\\Base\\')
        file = open(os.getcwd() + '\\Base\\UltimaBusquedaLog.txt', 'r')
        for line in file.readlines():
            if 'last_id' in line:
                last_id = int(line.split(":",1)[1])
            elif 'fist_id' in line:
                fist_id = int(line.split(":",1)[1])
        file.close()
        return last_id, fist_id
    except FileNotFoundError:
        return 0, 0

def guardarBusquedaLog(resumen):
    if not os.path.exists(os.getcwd() + '\\Base\\'):
        os.makedirs(os.getcwd() + '\\Base\\')
    file = open(os.getcwd() + '\\Base\\UltimaBusquedaLog.txt', 'w')
    file.writelines(resumen)
    file.close()

def generar_diccionario_afectos():
    diccionario_afectos = {}
    while not os.path.isfile(os.getcwd() + '\\Documentacion\\Diccionario_Afectos.csv'):
        input('Por favor, coloque el archivo "Diccionario_Afectos.csv" dentro de la carpeta Documentacion.\n'
              'Presione Enter cuando esté listo...')
    file = open('Documentacion\\Diccionario_Afectos.csv', 'r')
    reader = csv.reader(file, delimiter=';')

    for renglon in reader:
        if renglon[0][len(renglon[0]) - 1] != 'N':
            palabra = re.sub(r'(\_\w)?', '', renglon[0]) # Usa una expresión regular para identificar las palabras que finalicen con "_ + una letra cualquiera" y lo reemplaza por nada, es decir, lo corta.
            palabra = sbEsp.stem(palabra) # Normaliza la palabra
            diccionario_afectos[palabra] = float(renglon[1]) # int(puntaje) #Genera un diccionario cuya clave es una palabra normalizada y su valor representa el "score" de dicha palabra.

    return diccionario_afectos

def cargar_STOP_WORDS():
    try:
        STOP_WORDS = []
        while not os.path.isfile(os.getcwd() + '\\Documentacion\\STOP_WORDS.txt'):
            input('Por favor, coloque el archivo "STOP_WORDS.txt" dentro de la carpeta Documentacion.\n'
                  'Presione Enter cuando esté listo...')
        file = open(os.getcwd() + '\\Documentacion\\STOP_WORDS.txt', 'r', -1, 'utf-8')
        file.readline()
        for line in file.readlines():
            line = line.replace('\n','')
            STOP_WORDS.append(sbEsp.stem(line)) # Guarda la palabra normalizada
        file.close()
        return STOP_WORDS
    except FileNotFoundError:
        return ['URL','USER']

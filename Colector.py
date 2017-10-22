import Persistencia
import os
from Modelos import *

while not os.path.isfile(os.getcwd() + '\\Documentacion\\config.py'):
    input('Por favor, coloque el archivo "config.py" dentro de la carpeta Documentacion.\n'
          'Precione Enter cuando este listo...')
from Documentacion.config import *

class Colector():

    tw = None
    dicc = None
    last_id = None
    fist_id = None

    @staticmethod
    def Buscar():
        if Colector.tw == None:
            Colector.tw = Twitter(auth=OAuth(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY,
                                     CONSUMER_SECRET))  # Inicializo twitter con las credenciales
        if Colector.dicc == None:
            Colector.dicc = Persistencia.cargar()  # Cargo los tweets previamente guardamos
        if Colector.last_id == None or Colector.fist_id == None:
            Colector.last_id, Colector.fist_id = Persistencia.cargarBusquedaLog()  # Cargo ids para luego utlizar
        limite_alcanzado = False
        diccContador = {e.value: 0 for e in Candidato}  # Precargo los candidatos
        Colector.fist_id = Colector.last_id  # Guardo donde debo parar
        current_id = 0  # Guardo el último id que obtuve
        Colector.last_id = 0  # Voy a cambiarlo con el primer id de la próxima búsqueda
        while True:
            try:
                resultados = Colector.tw.search.tweets(
                    q=str(' OR ').join([e.value for e in Candidato]),
                    result_type='recent',
                    count=100,
                    max_id=current_id,
                    since_id=Colector.fist_id
                )
                limite_alcanzado = False #Reseteo el flag de limite de API
                for tweet in resultados['statuses']:
                    current_id = tweet['id']#Guardo el id que estoy procesando
                    if Colector.last_id == 0:#Si no tengo un last_id es que recien empece
                        Colector.last_id = tweet['id']#Lo guardo como el primero del ciclo
                    for candidato in [e.value for e in Candidato]:
                        if candidato in tweet['text'] and tweet['id'] not in Colector.dicc[candidato]:
                            diccContador[candidato] += 1
                            try:
                                Colector.dicc[candidato][tweet['id']] = {'Id': tweet['id'], 'Texto': tweet['text'],
                                                                     'Fecha': tweet['created_at']}
                            except KeyError:
                                Colector.dicc[candidato] = {tweet['id']: {'Id': tweet['id'], 'Texto': tweet['text'],
                                                                      'Fecha': tweet['created_at']}}
                if Colector.fist_id == 0 or len(resultados['statuses'])<=1:
                    break  # Si no tengo primer Id o si ya no sobrepaso la cantidad de tweets obtenidos por consulta
                yield Colector.getResumen(diccContador)
            except (TwitterError, TimeoutError) as ex:
                if not limite_alcanzado:#Evito que se muestre mas de una vez
                    yield Colector.getResumen(diccContador) + '\nError de conexión' if ex is TimeoutError else '\nLimite excedido'
                    limite_alcanzado = not limite_alcanzado
            except (KeyboardInterrupt):
                break
            except:
                yield Colector.getResumen(diccContador) + '\nError inesperado'
        resumen = Colector.getResumen(diccContador)
        yield resumen
        resumen += Colector.ids()
        while True:
            try:
                Persistencia.guardarBusquedaLog(resumen)
                Persistencia.guardar(Colector.dicc)
                break
            except (KeyboardInterrupt):
                print('Aguarde, guardando progreso.')
        print('Proceso Guardado')

    @staticmethod
    def getResumen(diccContador):
        totales = ''
        if Colector.dicc != None:
            for candidato, tweets in Colector.dicc.items():
                totales += candidato + ': ' + str(len(tweets)) + ' (+' + str(diccContador[candidato]) + ')\n'
            totales += 'Total: ' + str(sum([len(x) for x in Colector.dicc.values()])) + ' (+' + str(sum(diccContador.values())) + ')\n'
        return totales

    @staticmethod
    def ids():
        if Colector.last_id != None or Colector.fist_id != None:
            return 'last_id:' + str(Colector.last_id) + '\nfist_id:' + str(Colector.fist_id)

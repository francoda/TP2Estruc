from Documentacion.config import *
from Modelos import *
import os, time
import Persistencia
import Estadisticas
from enum import IntEnum

class Menu():

    def __init__(self):
        while True:
            self.limpiar()
            self.opcion_menu = self.leer_entero('Menú Principal: \n'
                                                   '1 - Estadísticas \n'
                                                   '2 - Búsqueda Única \n'
                                                   '3 - Búsqueda Automática \n'
                                                   '0 - Salir \n', True)
            if self.opcion_menu == Menu_Principal.ESTADISTICAS:
                print('Los datos se están procesando, aguarde por favor...')
                dicc = Estadisticas.leer_tweets()
                dicc = Estadisticas.puntuar_tweets(dicc)
                print('Estadísticas:')
                for candidato, puntaje in dicc.items():
                    print(candidato, ': ', '%.2f' % puntaje)
                input('Precione Enter para volver al menú...')
            elif self.opcion_menu == Menu_Principal.SALIR:
                break
            else:
                self.tw = Twitter(auth=OAuth(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))#Inicializo twitter con las credenciales
                self.dicc = Persistencia.cargar()#Cargo los tweets previamente guardamos
                self.last_id, self.fist_id = Persistencia.cargarEstadisticas()#Cargo ids para luego utlizar
                while True:
                    try:
                        self.Buscar()
                        if self.opcion_menu == Menu_Principal.BUSQUEDA_UNICA:
                            input('Precione Enter para volver al menú...')
                            break
                        else:
                            time.sleep(15)
                    except (KeyboardInterrupt):
                        break

    def Buscar(self):
        limite_alcanzado = False
        diccContador = {e.value: 0 for e in Candidato}  # Precargo los candidatos
        self.fist_id = self.last_id  # Guardo donde debo parar
        current_id = 0  # Guardo el último id que obtuve
        self.last_id = 0  # Voy a cambiarlo con el primer id de la próxima búsqueda
        while True:
            try:
                resultados = self.tw.search.tweets(
                    q=str(' OR ').join([e.value for e in Candidato]),
                    result_type='recent',
                    count=100,
                    max_id=current_id,
                    since_id=self.fist_id
                )
                limite_alcanzado = False #Reseteo el flag de limite de API
                for tweet in resultados['statuses']:
                    current_id = tweet['id']#Guardo el id que estoy procesando
                    if self.last_id == 0:#Si no tengo un last_id es que recien empece
                        self.last_id = tweet['id']#Lo guardo como el primero del ciclo
                    for candidato in [e.value for e in Candidato]:
                        if candidato in tweet['text'] and tweet['id'] not in self.dicc[candidato]:
                            diccContador[candidato] += 1
                            try:
                                self.dicc[candidato][tweet['id']] = {'Id': tweet['id'], 'Texto': tweet['text'],
                                                                     'Fecha': tweet['created_at']}
                            except KeyError:
                                self.dicc[candidato] = {tweet['id']: {'Id': tweet['id'], 'Texto': tweet['text'],
                                                                      'Fecha': tweet['created_at']}}
                if self.fist_id == 0 or len(resultados['statuses'])<=1:
                    break  # Si no tengo primer Id o si ya no sobrepaso la cantidad de tweets obtenidos por consulta
                self.limpiar()
                print(self.resumen(diccContador))
            except (TwitterError, TimeoutError) as ex:
                if not limite_alcanzado:#Evito que se muestre mas de una vez
                    print('Error de conexión' if ex is TimeoutError else 'Limite excedido')
                    limite_alcanzado = not limite_alcanzado
            except (KeyboardInterrupt):
                break
            except:
                print('Error inesperado')
        self.limpiar()
        resumen = self.resumen(diccContador)
        print(resumen)
        resumen += self.ids()
        while True:
            try:
                Persistencia.guardarEstadisticas(resumen)
                Persistencia.guardar(self.dicc)
                break
            except (KeyboardInterrupt):
                print('Aguarde, guardando progreso.')
        print('Proceso Guardado')

    def limpiar(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def resumen(self, diccContador):
        totales = ''
        for candidato, tweets in self.dicc.items():
            totales += candidato + ': ' + str(len(tweets)) + ' (+' + str(diccContador[candidato]) + ')\n'
        totales += 'Total: ' + str(sum([len(x) for x in self.dicc.values()])) + ' (+' + str(sum(diccContador.values())) + ')\n'
        return totales

    def ids(self):
        return 'last_id:' + str(self.last_id) + '\nfist_id:' + str(self.fist_id)

    def leer_entero(self, texto, tomar_valores=False):
        valor = ''
        while valor == '':
            try:
                valor = int(input(texto))
                if tomar_valores:
                    valores = [int(s) for s in texto.split() if s.isdigit()]
                    if valor in valores:
                        return valor
                    else:
                        raise IndexError
                else:
                    return valor
            except:
                print('Por favor, ingrese un número correspondiente al menú:' + str([int(s) for s in texto.split() if s.isdigit()]))
            valor = ''

class Menu_Principal(IntEnum):
    SALIR = 0
    ESTADISTICAS = 1
    BUSQUEDA_UNICA = 2
    BUSQUEDA_AUTOMATICA = 3

if __name__ == '__main__':
    Menu()

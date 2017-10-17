from Documentacion.config import *
from Modelos import *
import threading, os
import Persistencia
import Estadisticas

class Menu():

    def __init__(self):
        dicc = Estadisticas.leer_tweets()
        dicc = Estadisticas.puntuar_tweets(dicc)
        for candidato, puntaje in dicc.items():
            print(candidato, ': ', '%.2f' % puntaje)
        input('Precione Enter para iniciar...')
        self.limpiar()
        self.tw = Twitter(auth=OAuth(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))#Inicializo twitter con las credenciales
        self.dicc = Persistencia.cargar()#Cargo los tweets previamente guardamos
        self.last_id, self.fist_id = Persistencia.cargarEstadisticas()#Cargo ids para luego utlizar
        print(self.resumen({e.value:0 for e in Candidato}))#Imprimo un resumen de los previamente guardado
        self.Ciclo()#Metodo que se llama cada 15seg

    def Ciclo(self):
        limite_alcanzado = False
        diccContador = {e.value: 0 for e in Candidato}  # Precargo los candidatos
        self.fist_id = self.last_id  # Guardo donde debo parar
        current_id = 0  # Aca guardo el ultimo id que obtuve
        self.last_id = 0  # Voy a cambiarlo con el primer id de la proxima busqueda
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
                if self.fist_id == 0 or len(resultados['statuses'])<100:
                    break  # Si no tengo primer Id o si ya no sobrepaso la cantidad de tweets obtenidos por consulta
                self.limpiar()
                print(self.resumen(diccContador))
            except TwitterError:
                if not limite_alcanzado:#Evito que se muestre mas de una vez
                    print('Limite excedido')
                    limite_alcanzado = not limite_alcanzado
        self.limpiar()
        resumen = self.resumen(diccContador)
        print(resumen)
        resumen += self.ids()
        Persistencia.guardarEstadisticas(resumen)
        Persistencia.guardar(self.dicc)
        print('Proceso Guardado')
        threading.Timer(15, self.Ciclo).start()

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

if __name__ == '__main__':
    Menu()
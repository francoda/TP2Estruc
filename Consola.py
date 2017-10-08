from enum import Enum
from Documentacion.config import *
from datetime import date
import sched, time, os
import Persistencia

class Menu():

    def __init__(self):
        self.tw = Twitter(auth=OAuth(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
        self.dicc = Persistencia.cargar()
        self.resumen()
        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(20, 1, self.Ciclo, (self.s,))
        self.s.run()

    def Ciclo(self, sc):
        try:
            #Pido a la API los tweets
            resultados = self.tw.search.tweets(
                q=str(' OR ').join([e.value for e in Candidato]),
                result_type='recent',
                count=100)
            for tweet in resultados['statuses']:
                for candidato in [e.value for e in Candidato]:
                    if candidato in tweet['text']:
                        try:
                            self.dicc[candidato][tweet['id']] = tweet
                        except KeyError:
                            self.dicc[candidato] = {tweet['id']: tweet}
            #Imprimo resultados
            self.limpiar()
            self.resumen()
        except Exception as ex:
            Persistencia.guardar(self.dicc)
            input(str(ex) + '\n Preciona Enter para continuar...')
        self.s.enter(20, 1, self.Ciclo, (sc,))

    def limpiar(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def resumen(self):
        contador = 0
        for candidato, tweets in self.dicc.items():
            print(candidato, ': ', len(tweets))
            contador += len(tweets)
        print('Total: ', contador)

class Candidato(Enum):
    CFKARGENTINA = '@CFKArgentina'
    ESTEBANBULLRICH = '@estebanbullrich'
    SERGIOMASSA = '@SergioMassa'
    RANDAZZOF  = '@RandazzoF'
    NESTORPITROLA  = '@nestorpitrola'
    JORGETAIANA = '@JorgeTaiana'
    GLADYS_GONZALEZ = '@gladys_gonzalez'
    STOLBIZER = '@Stolbizer'
    ANDREADATRI = '@andreadatri'
    #FLORENCIACASAMIQUELA =

if __name__ == '__main__':
    Menu()
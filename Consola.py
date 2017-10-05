from enum import Enum
from Documentacion.config import *
from datetime import date
import sched, time, os
import Persistencia

class Menu():

    def __init__(self):
        self.tw = Twitter(auth=OAuth(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
        self.dicc = {}#= Persistencia.cargar()
        self.last_id = 0
        last_date = date.today()
        for candidato, tweets in self.dicc.items():
            if len(tweets) >= 100 and last_date > tweets[len(tweets)-100]['created_at']:
                last_date = tweets[len(tweets)-100]['created_at']
                self.last_id = last_date = tweets[len(tweets)-100]['id']
        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(20, 1, self.Ciclo, (self.s,))
        self.s.run()

    def Ciclo(self, sc):
        #Pido a la API los tweets
        resultados = self.tw.search.tweets(
            q=str(' OR ').join([e.value for e in Candidato]),
            result_type='recent',
            count=100)
        #Guado el primer Id
        fist_id = resultados['statuses'][0]['id']
        for tweet in resultados['statuses']:
            print(tweet['text'])
            #Me Fijo que no sea uno de los ultimos agregados
            if self.last_id == tweet['id']:
                break
            for candidato in [e.value for e in Candidato]:
                if candidato in tweet['text']:
                    lista = self.dicc.get(candidato, [])
                    lista.append(tweet)
                    self.dicc[candidato] = lista
        Persistencia.guardar(self.dicc)
        #Guardo el id mas reciente
        self.last_id = fist_id
        #Imprimo resultados
        contador = 0
        for candidato, tweets in self.dicc.items():
            print(candidato, ': ', len(tweets))
            contador += len(tweets)
        print('Total: ', contador)
        self.s.enter(20, 1, self.Ciclo, (sc,))

    def limpiar(self):
        os.system('cls' if os.name=='nt' else 'clear')

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
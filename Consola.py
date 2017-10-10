from enum import Enum
from Documentacion.config import *
from datetime import date
import sched, time, os
import Persistencia

class Menu():

    def __init__(self):
        self.tw = Twitter(auth=OAuth(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
        self.dicc = Persistencia.cargar()
        self.last_id, self.fist_id = Persistencia.cargarEstadisticas()
        self.resumen({e.value:0 for e in Candidato})
        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(15, 1, self.Ciclo, (self.s,))
        self.s.run()

    def Ciclo(self, sc):
        try:
            diccContador = {e.value:0 for e in Candidato}
            tweets = []
            #Pido a la API los tweets
            if self.last_id == 0:
                resultados = self.tw.search.tweets(
                    q=str(' OR ').join([e.value for e in Candidato]),
                    result_type='recent',
                    count=100)
            else:
                resultados = self.tw.search.tweets(
                    q=str(' OR ').join([e.value for e in Candidato]),
                    result_type='recent',
                    count=100,
                    since_id=self.last_id)
            if len(resultados['statuses']) > 0:
                self.last_id = resultados['statuses'][0]['id']
            for tweet in resultados['statuses']:
                for candidato in [e.value for e in Candidato]:
                    if candidato in tweet['text']:
                        tweets.append(ascii(tweet['text']))
                        diccContador[candidato] += 1
                        try:
                            self.dicc[candidato][tweet['id']] = {'Id':tweet['id'], 'Texto':tweet['text'], 'Fecha':tweet['created_at']}
                        except KeyError:
                            self.dicc[candidato] = {tweet['id']: {'Id':tweet['id'], 'Texto':tweet['text'], 'Fecha':tweet['created_at']}}
            #Imprimo resultados
            self.limpiar()
            self.resumen(diccContador)
            for tweet in tweets:
                print(tweet)
        except Exception as ex:
            input(str(ex) + '\n Preciona Enter para continuar...')
        Persistencia.guardar(self.dicc)
        print('Puede Cerrar')
        self.s.enter(15, 1, self.Ciclo, (sc,))

    def limpiar(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def resumen(self, diccContador):
        resumen = ''
        for candidato, tweets in self.dicc.items():
            resumen += candidato + ': ' + str(len(tweets)) + ' (+' + str(diccContador[candidato]) + ')\n'
        resumen += 'Total: ' + str(sum([len(x) for x in self.dicc.values()])) + ' (+' + str(sum(diccContador.values())) + ')\n'
        print(resumen)
        resumen += 'last_id:' + str(self.last_id) + '\nfist_id:' + str(self.fist_id)
        Persistencia.guardarEstadisticas(resumen)

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
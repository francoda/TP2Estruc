import os, time, operator
import Estadisticas
from Colector import *
from Modelos import *

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
                dicc = Estadisticas.puntuar_tweets()
                print('Estadísticas:')
                for candidato, puntaje in sorted(dicc.items(), key=operator.itemgetter(1), reverse=True):
                    print('%.2f' % puntaje, '-', candidatos_nombre_apellido[candidato])
                input('Precione Enter para volver al menú...')
            elif self.opcion_menu == Menu_Principal.SALIR:
                break
            else:
                while True:
                    try:
                        for resumen in Colector.Buscar():
                            self.limpiar()
                            print(resumen)
                        if self.opcion_menu == Menu_Principal.BUSQUEDA_UNICA:
                            input('Precione Enter para volver al menú...')
                            break
                        else:
                            time.sleep(15)
                    except (KeyboardInterrupt):
                        break

    def limpiar(self):
        os.system('cls' if os.name=='nt' else 'clear')

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

if __name__ == '__main__':
    Menu()

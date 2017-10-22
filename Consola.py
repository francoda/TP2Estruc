import time
import Estadisticas
from Colector import *
from Modelos import *

class Menu():

    def __init__(self):
        while True:
            self.limpiar()
            opcion_menu = self.leer_entero('Menú Principal: \n'
                                                   '1 - Estadísticas \n'
                                                   '2 - Búsqueda Única \n'
                                                   '3 - Búsqueda Automática \n'
                                                   '0 - Salir \n')
            if opcion_menu == Menu_Principal.ESTADISTICAS:
                self.limpiar()
                opcion_estadistica = self.leer_entero('Estadísticas: \n'
                                                   '1 - Cantidad de Tweets \n'
                                                   '2 - Promedio de Afectos \n'
                                                   '0 - Volver \n')
                if opcion_estadistica != Menu_TipoEstadistica.SALIR:
                    print('Los datos se están procesando, aguarde por favor...')
                if opcion_estadistica == Menu_TipoEstadistica.CANTIDAD:
                    max_len = 0
                    for candidato, cantidad in Estadisticas.cantidad_tweets():
                        if max_len == 0:
                            max_len = len(str(cantidad))
                        print(str(cantidad).rjust(max_len), '-', candidatos_nombre_apellido[candidato])
                elif opcion_estadistica == Menu_TipoEstadistica.PROMEDIO:
                    for candidato, puntaje in Estadisticas.puntuar_tweets():
                        print('%.2f' % puntaje, '-', candidatos_nombre_apellido[candidato])
                if opcion_estadistica != Menu_TipoEstadistica.SALIR:
                    input('Presione Enter para volver al menú...')
            elif opcion_menu == Menu_Principal.SALIR:
                break
            else:
                while True:
                    try:
                        for resumen in Colector.Buscar():
                            self.limpiar()
                            print(resumen)
                        if opcion_menu == Menu_Principal.BUSQUEDA_UNICA:
                            input('Presione Enter para volver al menú...')
                            break
                        else:
                            time.sleep(15)
                    except (KeyboardInterrupt):
                        break

    def limpiar(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def leer_entero(self, texto):
        valor = None
        while valor == None:
            try:
                valor = int(input(texto))
                if valor in [int(s) for s in texto.split() if s.isdigit()]:
                    return valor
                else:
                    raise IndexError
            except:
                print('Por favor, ingrese un número correspondiente al menú:' + str([int(s) for s in texto.split() if s.isdigit()]))
            valor = None

if __name__ == '__main__':
    Menu()

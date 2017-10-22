from enum import Enum, IntEnum

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

candidatos_nombre_apellido = {Candidato.CFKARGENTINA.value: 'Cristina Fernández de Kirchner',
                              Candidato.ESTEBANBULLRICH.value: 'Esteban Bullrich',
                              Candidato.SERGIOMASSA.value: 'Sergio Massa',
                              Candidato.RANDAZZOF.value: 'Florencio Randazzo',
                              Candidato.NESTORPITROLA.value: 'Néstor Pitrola',
                              Candidato.JORGETAIANA.value: 'Jorge Taiana',
                              Candidato.GLADYS_GONZALEZ.value: 'Gladys González',
                              Candidato.STOLBIZER.value: 'Margarita Stolbizer',
                              Candidato.ANDREADATRI.value: 'Andrea Datri'}

class Menu_Principal(IntEnum):
    SALIR = 0
    ESTADISTICAS = 1
    BUSQUEDA_UNICA = 2
    BUSQUEDA_AUTOMATICA = 3

class Menu_TipoEstadistica(IntEnum):
    SALIR = 0
    CANTIDAD = 1
    PROMEDIO = 2



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

class Menu_Principal(IntEnum):
    SALIR = 0
    ESTADISTICAS = 1
    BUSQUEDA_UNICA = 2
    BUSQUEDA_AUTOMATICA = 3


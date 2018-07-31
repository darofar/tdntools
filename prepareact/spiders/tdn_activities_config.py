import os

DIA0 = os.getenv("DIA0", "true")
DIA1 = os.getenv("DIA1", "true")
DIA2 = os.getenv("DIA2", "true")
DIA3 = os.getenv("DIA3", "true")
MANANA = os.getenv("MANANA", "true")
TARDE = os.getenv("TARDE", "true")
NOCHE = os.getenv("NOCHE", "true")
MAX_ITEMS = os.getenv("MAX_ITEMS", 20)

url_template = "http://jornadas-tdn.org/actividades/index?" \
   "dia0={dia0}&" \
   "dia1={dia1}&" \
   "dia2={dia2}&" \
   "dia3={dia3}&" \
   "manana={manana}&" \
   "tarde={tarde}&" \
   "noche={noche}&" \
   "max={max}&" \
   "offset={offset}".format(
        dia0=DIA0,
        dia1=DIA1,
        dia2=DIA2,
        dia3=DIA3,
        manana=MANANA,
        tarde=TARDE,
        noche=NOCHE,
        max=MAX_ITEMS,
        offset=0
    )

# Jornadas TdN - python tools

## Requisitos
Necesitas python 3.5+ para ejecutar los scripts que te vas a encontrar
en este compendio de herramientas. Es posible que prefieras crear un 
entorno virtual y lanzar los scripts desde es entorno. En todo caso 
necesitarás haber instalado las dependencias con el siguiente comando:

```bash
pip3 install -r requirements.txt
```

## Entornos por jornadas
Te recomiendo que crees un entorno virtual por cada jornada: tdn, rolea y 
zona lúdica. En cada uno de esos entornos podrás definir las siguientes 
variables de entorno:

    export USER_NAME=""
    export PASSWORD=""

## Inscripción

Este script te permite inscirbirte en las jornadas. Para ejecutarlo con 
éxito es necesario:
 - Disponer de un usuario y contraseña válidos.
 - Haber creado una habitación virtual con antelación. 
 - Definir la variable de entorno `INSCRIBE_URL="http://jornadas-tdn.org/virtual/ocupar"`

El script admite los siguientes parámetros   

```bash
python3 inscription.py -u USER_NAME -p PASSWORD -j JSESSIONID -h
```

-h: Imprime la ayuda del script.  
-u: Define el nombre de usuario para esta ejecución.  
-p: Define el password del usuario para esta ejecución.
-j: Define el JSESSIONID para esta ejecución.   

Para ejecutar el script es solo necesario definir nombre de usuario y 
contraseña. O bien el identificador de sesión. El script comprobará que 
el identificador de sesión ha sido definido, en caso de no estar definido 
utilizará las credenciales para obtener uno. 

También puedes ejecutar el script habiendo definido estos parámetros 
cómo variables de entorno. 

```bash
export USER_NAME=""
export PASSWORD=""
export JSESSION_ID=""
export INSCRIBE_URL=""
```

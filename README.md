# ASCP_Messenger

## Requerimientos

Se requiere tener instalado alguna versión de python3 en la computadora. 
Para la parte de encripción/desencripción, se necesita instalar la librería pyDES:

```
pip install pydes
```

## Contenido de las carpetas

El repositorio cuenta con dos ramas: ***main*** y *dev*. 
La rama *main* es donde están todos los cambios realizados hasta ahora. 

Dentro de ella cuenta con 4 archivos: `server.py`, `GUI.py`, `README.md` y `pruebas.py`. 

En el archivo `server.py`, es donde se encuentra la parte del código que se encarga de establecer la conexión entre las entidades, inicializando el socket. Es ahí donde se coloca el IP y puerto de la entidad local. A su vez, se define la configuración para recibir los mensajes y distribuirlos a las entidades *clientes* que están escuchando.

En el archivo `GUI.py`, se encuentra la sección que se encarga de la interfaz gráfica, además de conectarse con el servidor, escuchar, encriptar y desencriptar mensajes para enviar o recibir.

El `README.md` viene siendo este archivo donde se incluyen la información necesaria para comprender más a fondo la aplicación.

Por último, `pruebas.py` es donde se estuvieron haciendo pruebas para comprobar la funcionalidad de algunas funciones, sin embargo es irrelevante para el proyecto.


## Correr la app

Se usan los comandos (cada uno en una terminal distinta y en ese orden respectivamente): 

```
python3 Server.py 
python3 GUI.py
```

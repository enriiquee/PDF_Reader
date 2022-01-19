## *PDF reader*

This script allow to read OneFoundation files from different format

### *Instalar Python 3.*
Nos vamos a la página web de Python (https://www.python.org/ftp/python/3.9.1/python-3.9.1-macosx10.9.pkg). Se os descargará un archivo. Lo instaláis.

### *Ejecutar el programa*

#### *Windows*
Para realizar la instalación de los paquetes necesarios, abrimos la terminal de Windows. 
Una vez hecho esto, nos desplazamos a la carpeta donde habéis descomprimido el archivo que os he adjuntado. En windows/mac/linux, para desplazarte por los directorios, usamos el comando “cd”.
Por ejemplo, yo lo he descargado en el escritorio, por lo tanto uso cd Desktop/PDF_Reader . Si escribo el comando ls, aparecerá lo que tengo en esa carpeta. 

```
pip install -r /path/to/requirements.txt
```
Una vez instalados los paquetes, ejecutamos el siguiente comando: 

```python
python lanzador.py
```
En caso de que no funcione, probad con:

```python
python3 lanzador.py
```
Se abrirá una terminal donde seleccionamos el path donde están los archivos y le damos a run. 

#### *iOS*
Abrimos la terminal de iOS. Para ello pulsamos cmd+space y ponemos “Terminal”

Una vez hecho esto, vamos a instalar los paquetes que necesitamos para utilizar el script. Para ello usamos el siguiente comando:
```python
pip3 install -r requirements.txt
```
Una vez se haya instalado todo, finalmente se ejecuta el programa con el siguiente comando:
```python
python3 lanzador.py
```

Seleccionamos la carpeta y le dais a Run program. Y si no hay ningún inconveniente, se ejecutará y avisará cuando termine.

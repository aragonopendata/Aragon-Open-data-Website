#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       download1.py
#
#       Copyright 2013 Recursos Python - www.recursospython.com
#
#
from urllib2 import urlopen
def main():
    url = ("http://recursospython.com/wp-content/uploads/2013/08/"
           "compresion_y_descompresion.zip")
    # Archivo web
    r = urlopen(url)
    # Nombre del archivo a partir del URL
    filename = url[url.rfind("/") + 1:]
    while not filename:
        filename = raw_input("No se ha podido obtener el nombre del "
                             "archivo.\nEspecifique uno: ")
    print "Descargando %s..." % filename
    # Archivo local
    f = open(filename, "wb")
    # Escribir en un nuevo fichero local los datos obtenidos vía HTTP.
    f.write(r.read())
    # Cerrar ambos
    f.close()
    r.close()
    print "%s descargado correctamente." % filename
if __name__ == "__main__":
    main()

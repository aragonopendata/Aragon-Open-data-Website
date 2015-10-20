#!/bin/bash

echo 'Comienza a realizar el dump'

#activamos el enviroment

. /usr/lib/ckan/default/bin/activate

#ejecutamos el script
python /home/ams/pythonScripts/generaDUMPS/generaDumpsCKAN.py

#salimos del enviroment

deactivate

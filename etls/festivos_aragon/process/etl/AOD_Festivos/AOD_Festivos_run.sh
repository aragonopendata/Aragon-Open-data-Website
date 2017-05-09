#!/bin/sh
cd `dirname $0`
ROOT_PATH=`pwd`
java -Xms256M -Xmx1024M -cp .:$ROOT_PATH:$ROOT_PATH/../lib/routines.jar:$ROOT_PATH/../lib/log4j-1.2.16.jar:$ROOT_PATH/../lib/slf4j-api-1.7.5.jar:$ROOT_PATH/../lib/dom4j-1.6.1.jar:$ROOT_PATH/../lib/jxl.jar:$ROOT_PATH/../lib/talendcsv.jar:$ROOT_PATH/../lib/slf4j-simple-1.7.5.jar:$ROOT_PATH/../lib/hsqldb.jar:$ROOT_PATH/../lib/ical4j-2.0.0.jar:$ROOT_PATH/../lib/commons-lang3-3.4.jar:$ROOT_PATH/../lib/talend_file_enhanced_20070724.jar:$ROOT_PATH/../lib/commons-collections4-4.0.jar:$ROOT_PATH/../lib/json_simple-1.1.jar:$ROOT_PATH/aod_festivos_1_0.jar:$ROOT_PATH/aod_generaficherosfestivos_1_0.jar: festivosdga.aod_festivos_1_0.AOD_Festivos --context=Server "$@" 
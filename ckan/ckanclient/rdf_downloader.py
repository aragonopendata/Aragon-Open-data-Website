#!/usr/bin/python
import urllib
import sys
import os
import glob
import re
import config
import rdf_parser

def remove_files():
    print "Removing files from %s" % config.DOWNLOAD_PATH
    for old_file in glob.glob(config.DOWNLOAD_PATH + "/*.*"):
        os.remove(old_file)

def report_hook(a, b, c):
    print "% 3.1f%% of %d bytes\r" % (min(100, float(a * b) / c * 100), c)
    sys.stdout.flush()

def download(url):
    file = (url[url.rfind('/') + 1:]).rstrip('\n')

    if (file == "downloadIaest"):
        urllib.urlretrieve(url)
        print "URL:"+str(url)
    else:
        urllib.urlretrieve(url, config.DOWNLOAD_PATH + "/" + file, report_hook)

def extract_rdf(jsp):
    header = '<?xml version="1.0" encoding="utf-8"?>'
    write = False
    file = open(jsp)
    dest_file = re.sub("\.jsp", ".rdf", jsp)
    print  'Fichero de destino', dest_file
    
    print  'Fichero de jsp es', jsp
    dest = open(dest_file, 'wb')
    dest.write(header)
    for line in file:
        if '<rdf:RDF' in line:
            print 'Se comienza a escriber'
            write = True
        elif re.match("^ ?<\/rdf:", line):
            dest.write(line)
            write = False
        if write:
            if (line.find('&')>=0):
                line = line.replace('&', '&amp;')
            dest.write(line)
    file.close()
    dest.close()


def main():
    print "red_downloader"
    remove_files()
    urls = open(config.URL_FILE)
    for url in urls:
        print(url)
        download(url)
    print 'Comienza el extract'
    for jsp in glob.glob(config.DOWNLOAD_PATH + "/*.jsp"):
        extract_rdf(jsp)
    print 'Antes de parsear'
    print(rdf_parser.parse_rdfs());
    print 'Se finalizo la actualizacion de los datasets'
main()

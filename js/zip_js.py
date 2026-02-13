#!/usr/bin/env python 
#-*- coding: utf-8 -*-
#This script is used to compress javascript source code
import re #regexp module
import os #operational system module
import glob #filename globbing utility
import codecs

from jsmin import JavascriptMinify

js_files = glob.glob("./*_src.js")
jsm = JavascriptMinify()

for js_file in js_files:
    f = codecs.open(js_file,'r','utf-8')
    f2 = codecs.open(js_file.replace("_src",""),'w','utf-8')
    
    #Minify the javascript file
    jsm.minify(f, f2)
    
    #Close files
    f.close()
    f2.close()
    
    #Warn user that process has ended
    fsize = os.path.getsize(f.name)
    f2size = os.path.getsize(f2.name)
    print("-------------------------------------")
    print("Filename ["+js_file.replace("_src","")+"]")
    print("Compressed File = ",str(f2size).rjust(10)," bytes")
    print("    Source File = ",str(fsize).rjust(10)," bytes")
    if (fsize == 0): fsize = 1 #Avoiding ZeroDivisionError
    print("New size is %.2f%% of original size." % ((float(f2size)/float(fsize))*100.0))
print("-------------------------------------")
raw_input('Press Enter to quit...')

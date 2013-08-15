#!/usr/bin/env python 
#-*- coding: utf-8 -*-
# This script monitors file (watchdog) for changes and activate
# JavaScript compilation
import os, glob, time
import re #regexp module
import os #operational system module
import codecs

from jsmin import JavascriptMinify
jsm = JavascriptMinify()

def optimize(js_file):
    print "   -> Optimizing " + js_file + "..."
    f = codecs.open(js_file,'r','utf-8')
    f2 = codecs.open(js_file.replace("_src",""),'w','utf-8')
    
    #Minify the javascript file
    jsm.minify(f, f2)
    
    #Close files
    f.close();
    f2.close();
    
    #Warn user that process has ended
    fsize = os.path.getsize(f.name)
    f2size = os.path.getsize(f2.name)
    print "-------------------------------------"
    print "Filename ["+js_file.replace("_src","")+"]"
    print "Compressed File = ",str(f2size).rjust(10)," bytes"
    print "    Source File = ",str(fsize).rjust(10)," bytes"
    if (fsize == 0): fsize = 1 #Avoiding ZeroDivisionError
    print "New size is %.2f%% of original size." % ((float(f2size)/float(fsize))*100.0)

def main():
    path = './'
    files = '*_src.js'
    
    print """watch_js - watches for .js file changes
        
Watching path: %s
Watching files: %s
    """ % (path, files)
    
    first = True
    while True:
        date_file_list = []
        for folder in glob.glob(path):
            # select the type of file, for instance *.jpg or all files *.*
            for file in glob.glob(folder + files):
                # retrieves the stats for the current file as a tuple
                # (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)
                # the tuple element mtime at index 8 is the last-modified-date
                stats = os.stat(file)
                # create tuple (year yyyy, month(1-12), day(1-31), hour(0-23), minute(0-59), second(0-59),
                # weekday(0-6, 0 is monday), Julian day(1-366), daylight flag(-1,0 or 1)) from seconds since epoch
                # note:  this tuple can be sorted properly by date and time
                lastmod_date = time.localtime(stats[8])
                #print image_file, lastmod_date   # test
                # create list of tuples ready for sorting by date
                date_file_tuple = lastmod_date, file
                date_file_list.append(date_file_tuple)
            
        date_file_list.sort()
        date_file_list.reverse()  # newest mod date now first
      
        if first:
            print "Watching " + str(len(date_file_list)) + " files"
            print " "
            first = False
            
        keep = True
        while keep:
            for file in date_file_list:
                folder, file_name = os.path.split(file[1])
                stored_file_date = file[0]
                stats = os.stat(file[1])
                current_date = time.localtime(stats[8])
                file_date = time.strftime('%m/%d/%y %H:%M:%S', file[0])
                old_date = time.strftime('%m/%d/%y %H:%M:%S', current_date)
                changed = ' '
                if (stored_file_date < current_date):
                    print "   -> File " + file_name + " changed, rebuilding..."
                    keep = False
                    optimize(file_name)
            if keep:
                time.sleep(1) 

main()
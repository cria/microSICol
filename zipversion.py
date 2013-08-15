#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Renato Arnellas Coelho renatoac at gmail dot com
#
# Script to create Sicol's new version zip file
#
# Obs: This script must be run on Sicol's root directory 
import zipfile
import os
import sys
try:
  sys_version = str(int(raw_input("System Version number = ")))
  db_version = str(int(raw_input("Database Version number = ")))
except Exception,e:
  print "*********** ERROR ***********"
  print "Please type only numbers."
  raw_input()
  sys.exit(0)
#Create Empty Zip File (ZIP_STORED = no compression, ZIP_DEFLATED = compressed)
zip = zipfile.ZipFile('sicol_v'+sys_version+'.zip','w',zipfile.ZIP_DEFLATED)
#Read all files recursively, add them to zip file, avoid '.svn' folders
try:
  for root,dirs,files in os.walk(os.curdir):
    if root == os.curdir:
      files.remove('config.xml') #ignore personal configuration
    elif root == os.curdir+os.sep+'session':
      files = ['none'] #Don't get session files, only dummy file
    elif root == os.curdir+os.sep+'doc_file':
      files = ['none'] #Don't get uploaded files, only dummy file
    elif root == os.curdir+os.sep+'db':
      files.remove('sqlite.db') #ignore personal sqlite
    elif root == os.curdir+os.sep+'db'+os.sep+'scripts':
      #Get only the database scripts related to this version
      dirs = []
      if os.path.exists(os.path.join(root,'v'+db_version)):
        dirs = ['v'+db_version]
    if '.svn' in dirs:
      dirs.remove('.svn') #don't visit SVN directories
    for name in files:
      if name[-4:] != '.zip': #Don't get recursively any zip file!
        zip.write(os.path.join(root,name).replace('\\','/')[2:])
except Exception,e:
  print str(e)
  raw_input()
zip.close()
#Script finished
print "Zip completed."
raw_input()

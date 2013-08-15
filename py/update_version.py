#!/usr/bin/env python  
#-*- coding: utf-8 -*-
import cgitb;cgitb.enable() 
import os
from cgi import FieldStorage
from modules.general import General
from glob import glob
#Globals
MAIN_ACTION = 'get_version_number'
VALID_ACTIONS = ('get_version_number','get_version_zip_file')
#Get Current Version
g = General()
v = glob(os.path.join(g.get_config('root_dir'),'v[0-9][0-9][0-9]'))[0] #returns "/path/to/v123"
v = v.split(os.sep)
v = v[(len(v)-1)][1:] #get number only, e.g. "123"
#Get QUERY_STRING
query = FieldStorage()
action = MAIN_ACTION
if query.has_key('action'):
  action = query['action'].value
  if action not in VALID_ACTIONS:
    action = MAIN_ACTION
#Do the requested action
if action == 'get_version_number':
  #Print HTTP Header
  print "Content-Type: plain/text\n\n"
  #Print Content Body
  print v #receiver will have to trim this string
elif action == 'get_version_zip_file':
  #Print HTTP Header
  print "Content-Type: plain/text\n\n"
  #Print Content Body
  print open(os.path.join(g.get_config('root_dir'),'sicol_v'+str(v)+'.zip'),'rb').read()

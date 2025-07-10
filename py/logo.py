#!/usr/bin/env python3  
#-*- coding: utf-8 -*-
#
# Return image related to current collection
import cgitb; cgitb.enable()
#python imports
import sys
import base64
from .modules.cookie import Cookie
from .modules.session import Session
from .modules.dbconnection import dbConnection
from cgi import FieldStorage

if sys.platform == "win32":
    import os, msvcrt
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

#Print HTTP Header
print("Content-Type: image/png")
print()  # Empty line to separate headers from content

#Load GET data
form = FieldStorage()
#Load Cookie
cookie = Cookie()
cookie_value = cookie.read('Sicol_Session')
#Load Session
session = Session()
session.load(cookie_value)
#Connect to SQLite
db = dbConnection()
#Get Collection's Logo
id_coll = session.data['id_coll']
id_user = session.data['id_user']
try:
  id_coll = form['id'].value #Check whether there is any ID passed via GET method
  #Check whether user has access to this Collection
  db.execute('get_user_colls',{'id_user':id_user})
  colls = db.fetch('all')
  colls = [coll['id_coll'] for coll in colls]
  if (not int(id_coll) in colls) and (2 not in session.data['roles']): #Use default Logo then 
    id_coll = session.data['id_coll'] 
except Exception as e:
  pass
db.execute('get_coll_logo',{'id_coll':id_coll})
logo = db.fetch('one')
if logo == '':
  #Get default image
  from os import path
  from .modules.general import General
  g = General()
  img_dir = path.join(g.get_config('root_dir'), 'img')
  #For some reason, relative path does not work on IIS7-IE7-Win-Vista
  f = open(path.join(img_dir,'logo.png'),'rb')
  logo = f.read()
  f.close()
  sys.stdout.buffer.write(logo)
else:
  sys.stdout.buffer.write(base64.decodestring(logo))

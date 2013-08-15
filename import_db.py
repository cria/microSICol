#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script to import XML data to current SICol database
# Obs: This script must be executed on root directory
# Author:Renato Arnellas Coelho renatoac at gmail dot com
import sys
import os
from xml.dom.minidom import Document,parse
def importSQLite(xml,sqlite_path='./db/sqlite.db'):
  '''
  xml = XML filename
  sqlite_path = default is usually used
  '''
  from pysqlite2 import dbapi2 as sqlite
  print "Connecting to SQLite database..."
  if os.path.exists(sqlite_path):
    #Connect
    connect = sqlite.connect(sqlite_path,detect_types=sqlite.PARSE_COLNAMES,isolation_level=None)
    cursor = connect.cursor()
    print "Loading SQLite XML..."
    doc = parse(xml)
    tables = doc.getElementsByTagName('table')
    for table in tables:
      tablename = table.getAttribute('name')
      print "Emptying table '%s'..." % tablename
      rows = table.getElementsByTagName('row')
      cursor.execute("DELETE FROM %s;" % tablename) #clear table first
      print "Inserting values in table '%s'..." % tablename
      ### INSERT ITEM ###
      for row in rows:
        fields = row.getElementsByTagName('field')
        colnames = []
        colvalues = []
        for field in fields:
          colnames.append('`'+field.getAttribute('name')+'`')
          coltype = field.getAttribute('type')
          if coltype == 'integer':
            colvalues.append(field.getAttribute('value'))
          elif coltype == 'NULL':
            colvalues.append("NULL")
          else: #behaves as string
            colvalues.append("'"+field.getAttribute('value').replace("'","\\'")+"'")
        cursor.execute("INSERT INTO `%s` (%s) VALUES (%s);" % (tablename,",".join(colnames),",".join(colvalues) )  )  
      ###################
    #Close
    cursor.close()
    connect.close()
    print "*** Import Finished ***"
    raw_input()
  else:
    print "*** ERROR ***"
    print "Unable to connect to SQLite database."
    raw_input()

def importData(xml,host,user,pwd,dbname,port):
  '''
  xml = XML filename
  host = MySQL host
  user = MySQL root user
  pwd = MySQL root password
  dbname = MySQL database to be used
  port = MySQL port number
  '''
  import MySQLdb as mysql
  #Load file to Python XML object
  print "Loading XML..."
  doc = parse(xml)
  print "Generating intermediate SQL import file..."
  output = []
  #Connect to database
  output.append("USE %s;" % dbname)
  #Set Global VARS
  output.append("/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;")
  output.append("/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;")
  output.append("/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;")
  output.append("/*!40101 SET NAMES utf8 */;")
  output.append("/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;")
  output.append("/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;")
  output.append("/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;")
  output.append("")
  #Insert data in each table disabling key constrains
  tables = doc.getElementsByTagName('table')
  for table in tables:
    tablename = table.getAttribute('name')
    print "Reading table '%s'..." % tablename
    rows = table.getElementsByTagName('row')
    output.append("/*!40000 ALTER TABLE `%s` DISABLE KEYS */;" % tablename)
    output.append("TRUNCATE TABLE `%s`;" % tablename) #clear table first
    ### INSERT ITEM ###
    for row in rows:
      fields = row.getElementsByTagName('field')
      colnames = []
      colvalues = []
      for field in fields:
        colnames.append('`'+field.getAttribute('name')+'`')
        coltype = field.getAttribute('type')
        if coltype == 'integer':
          colvalues.append(field.getAttribute('value'))
        elif coltype == 'NULL':
          colvalues.append("NULL")
        else: #behaves as string
          colvalues.append("'"+field.getAttribute('value').replace("'","\\'")+"'")
      output.append("INSERT INTO `%s`.`%s` (%s) VALUES (%s);" % (dbname,tablename,",".join(colnames),",".join(colvalues) )  )  
    ###################
    output.append("/*!40000 ALTER TABLE `%s` ENABLE KEYS */;" % tablename)
  #Set Global VARS
  output.append("")
  output.append("/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;")
  output.append("/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;")
  output.append("/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;")
  output.append("/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;")
  output.append("/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;")
  output.append("/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;")
  output.append("/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;")
  #Save SQL file
  open('import.sql','w').write("\n".join(output).encode('utf-8'))
  print "Running SQL import..."
  sicol_path  = os.getcwd()+os.sep+'db'+os.sep+'scripts'+os.sep
  import platform
  if platform.system() == "Windows" or platform.system() == "Microsoft":
    mysql_path  = [x for x in os.environ['PATH'].split(";") if x.lower().find('mysql') != -1]
  else: #UNIX
    pipe = os.popen("which mysql") #grab where MySQL is installed
    mysql_path = pipe.read().strip() 
  if mysql_path == '' or mysql_path == []:
    print "*********** ERROR ***********"
    print "Please insert path to executable directory (mysql.exe) in OS 'PATH' variable."
    raw_input() #Wait for user input...
  else:
    if platform.system() == "Windows" or platform.system() == "Microsoft":
      #Ignore whether PATH ends with '\' or not
      mysql_path = mysql_path[0]
      if mysql_path[-1] != '\\': mysql_path += '\\'
      mysql_path = '"' + mysql_path + 'mysql.exe"'
  try:
    bd_version = dbname.split("_")[1]
  except Exception,e:
    print "*********** ERROR ***********"
    print "Please type \"sicol_v###\" where ### = version number."
    raw_input() #Wait for user input...
    return
  try:
    os.system("%s -h%s -u%s -p%s < %s"  % (mysql_path,host,user,pwd,os.getcwd()+os.sep+"import.sql") )
  except Exception,e:
    print "*********** ERROR ***********"
    print str(e)
    raw_input() #Wait for user input...
    return
  print "*** Import Finished ***"
  raw_input()

#If this script is called locally...
if __name__ == "__main__":
  print "*** Import SICol Database ***"
  opt = raw_input("Import MySQL data? (y/n)")[0].lower()
  if opt == 'y':
    import getpass
    import os.path
    host = raw_input("host=")
    port = raw_input("port=")
    root_login = raw_input("administrator login=")
    root_pwd = getpass.getpass("administrator password=")
    dbname = raw_input("database name=")
    xml = raw_input("import XML filename=")
    while not os.path.exists(xml) and xml != '':
      print "*** ERROR ***"
      print "Specified file does not exist!"
      xml = raw_input("import XML filename=")
    if xml != '':
      importData(xml,host,root_login,root_pwd,dbname,port)
  opt = raw_input("Import SQLite data? (y/n)")[0].lower()
  if opt == 'y':
    xml = raw_input("import XML filename=")
    while not os.path.exists(xml) and xml != '':
      print "*** ERROR ***"
      print "Specified file does not exist!"
      xml = raw_input("import XML filename=")
    if xml != '':
      importSQLite(xml)

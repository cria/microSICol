#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Renato Arnellas Coelho renatoac at gmail dot com
#
# Script to update Sicol database
#
# Warning:
# 1 - Add MySQL executable directory to system's PATH environment variable
# 2 - This script _MUST_ be executed on root directory
def updateDB(full_mode=True):
  '''
  full_mode = whether to update only DB structure (False) or all possible data (True)
  @return bool - True = OK! False = Error found
  '''
  import getpass
  import os
  import platform
  from sys import exit

  print("Updating MySQL database...")
  if platform.system() == "Windows" or platform.system() == "Microsoft":
    import winsound
  ####################
  # User data
  ####################
  dados = {}
  dados['mysql_login']  = raw_input("MySQL administrator login: ")
  dados['mysql_pwd']    = getpass.getpass("MySQL administrator password: ")
  dados['mysql_bd']     = raw_input("MySQL Database (e.g. 'sicol_v123'): ")
  dados['mysql_user']   = raw_input("Sicol login to MySQL (e.g. 'sicol'): ")
  ####################
  # Internal data
  ####################
  sicol_path  = os.getcwd()+os.sep+'db'+os.sep+'scripts'+os.sep
  if platform.system() == "Windows" or platform.system() == "Microsoft":
    mysql_path = [x for x in os.environ['PATH'].split(";") if x.lower().find('mysql') != -1]
  else: #UNIX
    pipe = os.popen("which mysql") #grab where MySQL is installed
    mysql_path = pipe.read().strip() 
  host        = "localhost"
  user        = dados['mysql_login']
  pwd         = dados['mysql_pwd']
  ####################
  # DB update script
  ####################
  if mysql_path == '' or mysql_path == []:
    print("*********** ERROR ***********")
    print("Please insert path to executable directory (mysql.exe) in OS 'PATH' variable.")
    raw_input() #Wait for user input...
    return False
  else:
    if platform.system() == "Windows" or platform.system() == "Microsoft":
      #Ignore whether PATH ends with '\' or not
      mysql_path = mysql_path[0]
      if mysql_path[-1] != '\\': mysql_path += '\\'
      mysql_path = '"' + mysql_path + 'mysql.exe"'
  try:
    bd_version = dados['mysql_bd'].split("_")[1]
  except Exception as e:
    print("*********** ERROR ***********")
    print("Please type \"sicol_v###\" where ### = version number.")
    raw_input() #Wait for user input...
    return False
  path_to_db = sicol_path + bd_version + os.sep
  # Load mysql_script_empty.sql
  dump_file = 'mysql_script_empty.sql'
  print("Loading database structure..." )
  try:
    os.system("%s -h%s -u%s -p%s < %s"  % (mysql_path,host,user,pwd,path_to_db+dump_file) )
  except Exception as e:
    print("*********** ERROR ***********")
    print(str(e))
    raw_input() #Wait for user input...
    
    #return False
  # Load mysql_start_dump.sql
  dump_file = "dump"+os.sep+"mysql_start_dump.sql"
  print("Loading initial dump to database..." )
  try:
    os.system("%s -h%s -u%s -p%s < %s"  % (mysql_path,host,user,pwd,path_to_db+dump_file) )
  except Exception as e:
    print("*********** ERROR ***********")
    print(str(e))
    raw_input() #Wait for user input...
    return False
  ######################
  # Load additional data
  ######################
  if full_mode:
    if platform.system() == "Windows" or platform.system() == "Microsoft":
      winsound.MessageBeep(winsound.MB_ICONASTERISK)
    opt = raw_input("Do you want to load test data? (y/n)\n")[0].lower()
    if opt == 'y':
      # Load mysql_testdata_dump.sql
      dump_file = "dump"+os.sep+"mysql_testdata_dump.sql"
      print("Loading test data to database..." )
      try:
        os.system("%s -h%s -u%s -p%s < %s"  % (mysql_path,host,user,pwd,path_to_db+dump_file) )
      except Exception as e:
        print("*********** ERROR ***********")
        print(str(e))
        raw_input() #Wait for user input...
        return
    if platform.system() == "Windows" or platform.system() == "Microsoft":
      winsound.MessageBeep(winsound.MB_ICONASTERISK)
    opt = raw_input("Do you want to load all Brazilian cities name to database? (y/n)\n")[0].lower()
    if opt == 'y':
      # Load mysql_cities_dump.sql
      dump_file = "dump"+os.sep+"mysql_cities_dump.sql"
      print("Loading Brazilian cities name to database..." )
      try:
        os.system("%s -h%s -u%s -p%s < %s"  % (mysql_path,host,user,pwd,path_to_db+dump_file) )
      except Exception as e:
        print("*********** ERROR ***********")
        print(str(e))
        raw_input() #Wait for user input...
        return
    if platform.system() == "Windows" or platform.system() == "Microsoft":
      winsound.MessageBeep(winsound.MB_ICONASTERISK)
    opt = raw_input("Do you want to load debug data? (y/n)\n")[0].lower()
    if opt == 'y':
      # Load mysql_cities_dump.sql
      dump_file = "dump"+os.sep+"mysql_debug_dump.sql"
      print("Loading debug data to database..." )
      try:
        os.system("%s -h%s -u%s -p%s < %s"  % (mysql_path,host,user,pwd,path_to_db+dump_file) )
      except Exception as e:
        print("*********** ERROR ***********")
        print(str(e))
        raw_input() #Wait for user input...
        return
  ########################
  # End of additional data
  ########################
  # Give database permissions to "sicol" user
  print("Transfering access permission to user \"%s\"..." % dados['mysql_user'])
  try:
    #Create temp file in order to change user permissions
    f = open('temp_user_access_bd.sql','w')
    f.write("GRANT ALL PRIVILEGES ON `%s`.* TO '%s'@localhost IDENTIFIED BY '%s';FLUSH PRIVILEGES;" % (dados['mysql_bd'].replace("_","\\_"),dados['mysql_user'],dados['mysql_user']))
    f.close()
    os.system("%s -h%s -u%s -p%s < %s"  % (mysql_path,host,user,pwd,os.getcwd()+os.sep+'temp_user_access_bd.sql') )
    os.unlink('temp_user_access_bd.sql')
  except Exception as e:
    print("*********** ERROR ***********")
    print(str(e))
    raw_input() #Wait for user input...
    return
  ####################
  # End of update
  ####################
  if platform.system() == "Windows" or platform.system() == "Microsoft":
    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
  print("****************************")
  raw_input("Update finished. Press [ENTER] to continue.")

#If this script is called locally...
if __name__ == "__main__":
  print("*** Update SICol Database ***")
  updateDB()
  print("*** Update Finished ***")

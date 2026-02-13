#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zipfile
import os
import sys
import glob
import urllib2

class SicolUpdate(object):
  '''
  Script to update SICol version.
  
  Obs: This script must be run on Sicol's root directory 
  - Files that must be within the same directory as this one: v123 (version file), 
  export.py, import_db.py, updated_external_db.py 
  Author:Renato Arnellas Coelho renatoac at gmail dot com
  '''
  #URL to where to check for updates
  SICOL_SERVER = "http://localhost/Sicol/py/update_version.py?"
  SICOL_VERSION = SICOL_SERVER + "action=get_version_number"
  SICOL_ZIPFILE = SICOL_SERVER + "action=get_version_zip_file"
  #Host and port number to access local database
  LOCAL_HOST = "localhost"
  LOCAL_PORT = "3306"
  #Attributes
  my_version = 0
  my_db_version = 0
  external_version = 0
  external_db_version = 0
  protect_file = ''
  mysql_backup = ''

  def __init__(self):
    print("***** SICOL UPDATE *****")
    print("Default Server Path = '%s'" % self.SICOL_SERVER)
    if self.ask("Do you want to change server path?"):
      self.SICOL_SERVER = raw_input("Type path:")
      #User may forget ending question mark
      if self.SICOL_SERVER[-1] != '?': self.SICOL_SERVER += '?'
      self.SICOL_VERSION = self.SICOL_SERVER + "action=get_version_number"
      self.SICOL_ZIPFILE = self.SICOL_SERVER + "action=get_version_zip_file"
      
  def ask(self,msg):
    '''
    Ask user a yes/no question
    '''
    opt = raw_input(msg+" (y/n)\n")
    if opt == '': return False
    opt = opt[0].lower()
    if opt == 'y': return True
    else: return False

  def error(self,msg):
    '''
    Notify user and wait for response
    '''
    print("***** ERROR *****")
    print(msg)
    #Wait for user response
    print("Press [Enter] to continue...")
    raw_input()
    
  def getLocalVersion(self):
    '''
    Checks user version. Returns false if any error occurs.
    '''
    try:
      self.my_version = glob.glob('v[0-9][0-9][0-9]')
      self.my_version = int(self.my_version[0][1:])
    except Exception as e:
      self.error("Version File not found.")
      return False
    return True

  def getRemoteVersion(self):
    '''
    Get latest version from SICOL SERVER
    '''
    try:
      f = urllib2.urlopen(self.SICOL_VERSION)
      #Download
      self.external_version = int(f.read().strip())
    except Exception as e:
      self.error("Connection to Remote Server failed.")
      return False
    return True

  def downloadZip(self):
    '''
    Download Zip File
    '''
    try:
      f = urllib2.urlopen(self.SICOL_ZIPFILE)
      #Save on currect directory
      open('latest_version.zip','wb').write(f.read().strip())
    except Exception as e:
      self.error(str(e))
      return False
    return True

  def deleteFiles(self):
    '''
    Read all files recursively, avoid removing special files
    '''
    try:
      for root,dirs,files in os.walk(os.curdir):
        if root == '.':
          if 'po' in dirs:
            dirs.remove('po') #avoid removing 'po' folder    
          if 'doc_file' in dirs:
            dirs.remove('doc_file') #avoid removing 'doc_file' folder    
          if 'session' in dirs:
            dirs.remove('session') #avoid removing 'session' folder
          if 'config.xml' in files:
            files.remove('config.xml') #avoid removing 'config.xml' configuration file
          if 'SICol_update.py' in files:
            files.remove('SICol_update.py') #avoid removing this very script file!
          if 'latest_version.zip' in files:
            files.remove('latest_version.zip') #avoid removing zip file
          if self.protect_file != '':
            if self.protect_file in files:
              files.remove(self.protect_file) #avoid removing recently created backup XML
        elif root == os.path.join('.','db','scripts'):
          #Get user latest database version
          dirs.sort()
          self.my_db_version = int(dirs[-1][1:]) #get last element, ignore first char
        #Remove unfiltered files
        for name in files:
          os.remove(os.path.join(root,name))
    except Exception as e:
      self.error(str(e))
      return False
    return True

  def unzipPackage(self):
    '''
    Unzip package
    '''
    try:
      zip = zipfile.ZipFile('latest_version.zip','r')
      for item in zip.namelist():
        root,name = os.path.split(item)
        if root != '' and not os.path.isdir(root): #Directory not found, create it
          os.makedirs(root)
        if root.startswith('db/scripts/v') and root[-1] != 'p': #Get zip file's latest db version
          db_v = int(root[-3:])
          if db_v > self.external_db_version:
            self.external_db_version = db_v 
        open(os.path.join(os.curdir,root,name),'wb').write(zip.read(item))
    except Exception as e:
      self.error(str(e))
      return False
    return True

  def run(self):
    '''
    Main execution
    '''
    #Start execution
    print("Checking for SICol version...")
    #Get my version
    if self.getLocalVersion() and self.getRemoteVersion():
      print("Local  version number is " + str(self.my_version) + ".")
      print("Remote version number is " + str(self.external_version) + ".")
      if (self.external_version <= self.my_version):
        print("You already have the latest version installed.")
      else:
        #Update SICol
        print("Downloading latest version...")
        if self.downloadZip():
          if self.ask("Do you want to export your personal SQLite database?"):
            import export as exp
            xml_filename = exp.exportSQLite()
            print("'%s' created." % xml_filename)
            self.protect_file = xml_filename
          if self.ask("System is about to delete old version files. Continue?"):
            #Delete old files
            print("Deleting old version files...")
            if self.deleteFiles():
              print("Unpacking update...")
              if self.unzipPackage():
                #Check whether there has been any database changes or not
                if self.external_db_version <= self.my_db_version:
                  print("Database is up-to-date.")
                else:
                  print("Your database is outdated." )
                  print("Local  database version = %s." % str(self.my_db_version))
                  print("Remote database version = %s." % str(self.external_db_version))
                  if self.ask("Do you want to export your current data?"):
                    import getpass
                    print("Default Local Host / Port number = '%s' / %s" % (self.LOCAL_HOST,self.LOCAL_PORT))
                    if self.ask("Do you want to change local host / port number?"):
                      self.LOCAL_HOST = raw_input("HOST=")
                      self.LOCAL_PORT = raw_input("PORT=")
                    root_login = raw_input("Administrator Login=")
                    root_pwd = getpass.getpass("Administrator Password=")
                    dbname = 'sicol_v'+str(self.my_db_version)
                    import export as exp
                    self.mysql_backup = exp.exportData(self.LOCAL_HOST,root_login,root_pwd,dbname,self.LOCAL_PORT)
                    print("'%s' created." % self.mysql_backup)
                  #Update new database
                  import update_external_db as upd
                  upd.updateDB(False)
                  if self.ask("Do you want to import MySQL data from a XML backup?"):
                    import import_db as imp
                    import getpass
                    import os.path
                    print("Default Local Host / Port number = '%s' / %s" % (self.LOCAL_HOST,self.LOCAL_PORT))
                    if self.ask("Do you want to change local host / port number?"):
                      self.LOCAL_HOST = raw_input("HOST=")
                      self.LOCAL_PORT = raw_input("PORT=")
                    root_login = raw_input("Administrator Login=")
                    root_pwd = getpass.getpass("Administrator Password=")
                    dbname = raw_input("Database name (e.g. 'sicol_v101')=")
                    if self.mysql_backup != '':
                      if self.ask("Do you want to use recently created '%s' file?" % self.mysql_backup):
                        xml = self.mysql_backup
                      else:
                        xml = raw_input("XML filename=")
                    while not os.path.exists(xml) and xml != '':
                      print("*** ERROR ***")
                      print("Specified file does not exist!")
                      xml = raw_input("XML filename=")
                    if xml != '':
                      imp.importData(xml,self.LOCAL_HOST,root_login,root_pwd,dbname,self.LOCAL_PORT)
                  if self.ask("Do you want to import SQLite data from a XML backup?"):
                    import import_db as imp
                    if self.protect_file != '':
                      if self.ask("Do you want to use recently created '%s' file?" % self.protect_file):
                        xml = self.protect_file
                      else:
                        xml = raw_input("XML filename=")
                    while not os.path.exists(xml) and xml != '':
                      print("*** ERROR ***")
                      print("Specified file does not exist!")
                      xml = raw_input("XML filename=")
                    if xml != '':
                      imp.importSQLite(xml)
          print("***** EXECUTION FINISHED *****")
          print("Press [Enter] to continue...")
          raw_input()

#If this script is called locally...
if __name__ == "__main__":
  sicol = SicolUpdate()
  sicol.run()

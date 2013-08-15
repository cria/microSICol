#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Renato Arnellas Coelho renatoac at gmail dot com
#
# Script to export to XML current SICol database data
# XML format example:
# <?xml version="1.0" ?>
# <database name="sicol_v104">
# 	<table name="strain">
# 		<row>
# 			<field name="is_ogm" value="0"/>
# 			<field name="code" value="14"/>
# 			<field name="id_strain" value="1"/>
# 			<field name="extra_codes" value="None"/>
# 			<field name="go_catalog" value="0"/>
# 			<field name="comments" value="None"/>
# 			<field name="id_coll" value="1"/>
# 			<field name="id_subcoll" value="1"/>
# 			<field name="id_type" value="None"/>
# 			<field name="last_update" value="2006-12-19 12:34:50"/>
# 			<field name="infra_complement" value="None"/>
# 			<field name="id_species" value="1"/>
# 			<field name="history" value="None"/>
# 		</row>
#     <row>...</row>
#   </table>
#   <table>...</table>
# </database>
from xml.dom.minidom import Document
def exportData(host,user,pwd,dbname,port):
  '''
  host = MySQL host
  user = MySQL root user
  pwd = MySQL root password
  dbname = MySQL database to be used
  port = MySQL port number
  '''
  #########
  # MySQL #
  #########
  import MySQLdb as mysql
  doc = Document()
  doc_db = doc.createElement("database")
  doc_db.setAttribute("name",dbname)
  doc.appendChild(doc_db)
  try:
    #Connect to database
    print "Connecting to database..."
    connect = mysql.connect(host, user, pwd, dbname, int(port), use_unicode=True, charset='utf8')
    cursor = mysql.cursors.DictCursor(connect)
    #Get all available TABLES
    cursor.execute("SHOW TABLES")
    all_tables = cursor.fetchall() #Returns ({'Tables_in_sicol_v123':...},{'...':'...'},{...},...)
    print "Creating XML from all " + str(len(all_tables)) + " tables..."
    for one_table in all_tables:
      tablename = one_table.values()[0]
      print "Parsing table '%s'..." % tablename
      doc_table = doc.createElement("table")
      doc_table.setAttribute("name",tablename)
      doc_db.appendChild(doc_table)
      cursor.execute("SELECT * FROM %s" % tablename)
      rows = cursor.fetchall()
      for row in rows:
        doc_row = doc.createElement("row")
        doc_table.appendChild(doc_row)
        for fieldname,fieldvalue in row.items():
          doc_field = doc.createElement("field")
          doc_field.setAttribute("name",fieldname)
          if fieldvalue is None:
            #NULL pointer
            doc_field.setAttribute("type","NULL")
            fieldvalue = "NULL"
          elif isinstance(fieldvalue,basestring):
            #String or Unicode
            doc_field.setAttribute("type","string") 
          elif isinstance(fieldvalue,int) or isinstance(fieldvalue,long):
            #Integer
            doc_field.setAttribute("type","integer") 
            fieldvalue = str(fieldvalue)
          else:
            #Consider it to behave as string
            doc_field.setAttribute("type","string") 
            fieldvalue = str(fieldvalue)
          doc_field.setAttribute("value",fieldvalue)
          doc_row.appendChild(doc_field)
    #Close
    cursor.close()
    connect.close()
    #Save XML
    print "Saving XML..."
    import datetime
    today_str = str(datetime.datetime.today())[:-7].replace(":","").replace(" ","_").replace("-","_") + '.xml'
    xml = doc.toprettyxml().encode('utf-8')
    f = open(today_str,'w')
    f.write(xml)
    f.close()
  except mysql.Error, e:
    print str(e)
    return
  except Exception,e:
    print str(e)
    return
  print "*** Export Finished ***"
  return today_str

def exportSQLite():
  ##########
  # SQLite #
  ##########
  import os
  from pysqlite2 import dbapi2 as sqlite
  sqlitedb = os.path.join(os.curdir,'db','sqlite.db')
  print "Connecting to SQLite database..."
  if os.path.exists(sqlitedb):
    doc = Document()
    doc_db = doc.createElement("database")
    doc_db.setAttribute("name","sqlite")
    doc.appendChild(doc_db)
    #Connect
    connect = sqlite.connect(sqlitedb,detect_types=sqlite.PARSE_COLNAMES,isolation_level=None)
    cursor = connect.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
    all_tables = cursor.fetchall()
    for table in all_tables:
      table = table[0] #items are inside a tuple
      print "Parsing table '%s'..." % table
      cursor.execute('SELECT * FROM %s' % table)
      rows = cursor.fetchall()
      cols = [x[0] for x in cursor.description]
      doc_table = doc.createElement("table")
      doc_table.setAttribute("name",table)
      doc_db.appendChild(doc_table)
      for row in rows:
        doc_row = doc.createElement("row")
        doc_table.appendChild(doc_row)
        i = 0
        for col_name in cols:
          col_value = row[i]
          doc_field = doc.createElement("field")
          doc_field.setAttribute("name",col_name)
          if col_value is None:
            #NULL pointer
            doc_field.setAttribute("type","NULL")
            col_value = "NULL"
          elif isinstance(col_value,basestring):
            #String or Unicode
            doc_field.setAttribute("type","string") 
          elif isinstance(col_value,int) or isinstance(col_value,long):
            #Integer
            doc_field.setAttribute("type","integer") 
            col_value = str(col_value)
          else:
            #Consider it to behave as string
            doc_field.setAttribute("type","string") 
            col_value = str(col_value)
          doc_field.setAttribute("value",col_value)
          doc_row.appendChild(doc_field)
          i += 1
    #Close
    cursor.close()
    connect.close()
    #Save XML
    print "Saving SQLite XML..."
    import datetime
    today_str = str(datetime.datetime.today())[:-7].replace(":","").replace(" ","_").replace("-","_") + '_sqlite.xml'
    xml = doc.toprettyxml().encode('utf-8')
    f = open(today_str,'w')
    f.write(xml)
    f.close()
  else:
    print "*** ERROR ***"
    print "Could not connect to SQLite database"
    raw_input()
    return
  print "*** Export Finished ***"
  return today_str

#If this script is called locally...
if __name__ == "__main__":
  print "*** Export SICol Database ***"
  opt = raw_input("Export MySQL data? (y/n)")[0].lower()
  if opt == 'y':
    import getpass
    host = raw_input("host=")
    port = raw_input("port=")
    root_login = raw_input("administrator login=")
    root_pwd = getpass.getpass("administrator password=")
    dbname = raw_input("database name=")
    exportData(host,root_login,root_pwd,dbname,port)
  opt = raw_input("Export SQLite data? (y/n)")[0].lower()
  if opt == 'y':
    exportSQLite()

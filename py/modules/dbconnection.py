#!/usr/bin/env python 
#-*- coding: utf-8 -*-

#python imports
from sys import exit
#from dbgp.client import brk

#project imports
import exception
from sql import Sql
from session import Session
from general import General
from loghelper import Logging

class dbConnection(object):

    g = General()    
    
    def __init__(self, cookie_value=None, base_descr=None):
        self.__fetchall = ''
        self.rows = 0
        self.connect = None
        self.sql = None

        #brk(host="localhost", port=9000)
        
        if cookie_value or base_descr:
            if cookie_value:
                #Load Session variables
                self.session = Session()
                self.session.load( cookie_value )
                host = self.session.data['db_host']
                port = self.session.data['db_port']
                dbname = self.session.data['db_name']
                user = self.session.data['db_user']
                pwd = self.session.data['db_pwd']
                self.dbms = self.session.data['dbms']
                self.sql = Sql(self.dbms)
            else:
                host = base_descr['host']
                port = base_descr['port']
                dbname = base_descr['db_name']
                user = base_descr['user']
                pwd = base_descr['pwd']
                self.dbms = base_descr['dbms']
                self.sql = Sql(self.dbms)

            self.logger = Logging.getLogger("dbconnection", extra=dbname)

            #Connect in instance
            import MySQLdb as mysql
            try: self.connect = mysql.connect(host, user, pwd, dbname, port, use_unicode=True, charset='utf8')
            except mysql.Error, e:
                import traceback
                self.logger.error("Error while connecting to MySQL: %s", traceback.format_exc(e))

                out = '%s%s' % (self.g.get_config('http_header'), '\n\n')
                out += "%s %d: %s" % (_('Error'), e.args[0], e.args[1])
                if (e.args[0] == 1045): #Error - Access Denied on MySQL database
                  out += self.g.read_html('login_check') % -3
                if (e.args[0] == 1044): #Error - Access denied for user 'sicol'@'%' to database 'sicol_v100'
                  out += self.g.read_html('login_check') % -6
                elif (e.args[0] == 2003): #Error - MySQL database has not been activated
                  out += self.g.read_html('login_check') % -4
                else:
                  out += self.g.read_html('login_check') % 0
                print out
                exit(1)
        else:
            self.logger = Logging.getLogger("dbconnection")
        
            #Connect in sqlite.db
            from os import path
            try:
                from pysqlite2 import dbapi2 as sqlite
            except ImportError:
                import sqlite3 as sqlite
            sqlitedb = path.join(self.g.get_config('root_dir'),'db','sqlite.db')
            if path.exists(sqlitedb):
                self.connect = sqlite.connect(sqlitedb,detect_types=sqlite.PARSE_COLNAMES,isolation_level=None)
                self.dbms = 'sqlite'
                self.sql = Sql(self.dbms)
            else:
                out = '%s%s' % (self.g.get_config('http_header'), '\n\n')
                out += '%s\n<br />%s %s' % (_("Sqlite Connection Failed!"), _("This database file does not exist:"), sqlitedb)
                print out
                exit(1)

        if self.dbms == "mysql":
            self.cursor = mysql.cursors.DictCursor(self.connect)
        else:
            self.cursor = self.connect.cursor()

    def getrows(self):
    
        return self.rows

    def fetch(self, mode, colname = ""):
        data = []
        all = self.__fetchall
        try:
            if (mode == 'one'):
                if colname:
                    try: data = all[0][colname]
                    except IndexError: data = ''
                else:
                    try: data = all[0][all[0].keys()[0]]
                    except IndexError: data = ''
            elif (mode == 'columns'):
                data = {}
                for x in all[0]:
                    data[x] = all[0][x]
            elif (mode == 'rows'):
                for x in all:
                    data.append(x.values()[0])
            elif (mode == 'all'):
                data = self.__fetchall[:]
        except IndexError:
            if isinstance (data, dict):
                data[colname] = ''
            elif isintance (data, list):
                data.append({colname:''})
            else:
                data = 'You should not be reading this!'
        #Replace NoneTypes
        data = self.g.replace_nonetypes(data)
        return data

    def execute(self, sqlfunction, vars = None, raw_mode = False, force_debug = False, fixed_sql = None):
        """
        Does the actual SQL manipulation. Sqlfunction is read from the proper
        xml file, and vars should be a dictionary with the substitutions to be
        perfomed in the query.
        """
        
        if fixed_sql != None:
            sql_line = fixed_sql    
        else:
            sql_line = self.sql.get(sqlfunction)
        
        if vars:
            values = vars.copy()
            for key in values:
                if values[key] == '' and self.dbms != 'sqlite': values[key] = None
            #We need to do this in separate, because table names are needed
            # in the "from" clause of the query, and cannot be quoted with "'"
            # the execute method of the cursor always quotes the parameters.
            if values.has_key("table"):
                sql_line = sql_line.replace("%(table)s", values["table"])
        else:
            if fixed_sql != None:
                values = None
            else:
                values = {}

        if self.dbms == 'sqlite':
            try:
                if (raw_mode):
                  #Special case - insert/update coll
                  import re
                  sql_line = re.sub("'\%.*?\)s'","?",str(sql_line))
                  self.logger.debug("[sqlite: %s] [%s]" % (sqlfunction, sql_line))
                  if values.has_key('coll_id'):
                    self.rows = self.cursor.execute(sql_line,(values['coll_base'],values['coll_code'],values['coll_name'],values['coll_logo'],values['coll_id']) )
                  else:
                    self.rows = self.cursor.execute(sql_line,(values['coll_base'],values['coll_code'],values['coll_name'],values['coll_logo']) )
                else:
                  if values is not None:
                    sql_line = sql_line % values
                  self.logger.debug("[sqlite: %s] [%s]" % (sqlfunction, sql_line))
                  self.rows = self.cursor.execute(sql_line)

                col_names = self.cursor.description
                if col_names is None:
                    self.__fetchall = []
                else:
                    data_dicts = []
                    for line in self.cursor.fetchall():
                        data_dict = {}
                        for i in xrange (len(line)):
                            data_dict[col_names[i][0]] = line[i]
                        data_dicts.append (data_dict)
                    self.__fetchall = data_dicts

            except Exception, e:
                self.logger.exception("[sqlite: %s] %s: %s" % (sqlfunction, str(e), sql_line))
                if str(e) == 'column login is not unique': #treat differently
                  raise exception.SicolSQLException (str(e))
                else:
                  raise exception.SicolSQLException ("%s: %s" % (_("Error in SQLite execute"), e), 1, "%s: %s\n<br />%s: %s" % (_("Sql function"), sqlfunction, _("Sql line"), sql_line))
        elif self.dbms == 'mysql':
            #raise str(sql_line) + ' v: ' + str(values) #line for debug
            try:                
                if (raw_mode):
                  if (force_debug):
                    self.logger.info("[mysql: %s] [%s]" % (sqlfunction, str(sql_line) % values))
                  self.logger.debug("[mysql: %s] [%s]" % (sqlfunction, str(sql_line) % values))
                  self.rows = self.cursor.execute(str(sql_line) % values)
                else:
                  if force_debug:
                    try:
                        self.logger.error("[mysql: %s] [%s]" % (sqlfunction, str(sql_line) % values))
                    except Exception, e:
                        self.logger.error("[mysql: %s] [%s] \nwith values: %s" % (sqlfunction, sql_line, str(values)))
                  else:
                    try:
                        self.logger.debug("[mysql: %s] [%s]" % (sqlfunction, str(sql_line) % values))
                    except Exception, e:
                        self.logger.debug("[mysql: %s] [%s] \nwith values: %s" % (sqlfunction, sql_line, str(values)))
                  
                  self.rows = self.cursor.execute(sql_line, values)
            except Exception, e:
                self.logger.error("[mysql: %s] %s: %s \nwith values: %s" % (sqlfunction, str(e), str(sql_line), str(values)))
                if e.args[0] == 1062: #"Duplicate entry '%d' for key 2" where %d = duplicated value
                  duplicated_value = e.args[1][17:e.args[1].rfind("'")]
                  raise Exception("%s: %s (%s)" % (_("Duplicate entry"), duplicated_value.decode('utf8'), sql_line.decode('utf8')))
                elif e.args[0] == 1451: #Cannot delete/update due foreign key constrain
                  import re
                  table_name = re.search(r"REFERENCES `(\w+?)`",e.args[1]).group(1)
                  if table_name == 'species':
                    raise exception.SicolException(_("Unable to delete due associations with table \"Strains\""))
                  else:
                    foreign_table_name = re.search(r"fails \(.*?/(\w+?)`",e.args[1]).group(1)
                    raise exception.SicolException(_("Unable to update/delete due foreign key constrain")+' - '+_("Foreign Table Name")+': '+foreign_table_name)
                else:
                  raise exception.SicolException("%s: %s" % (_("Error in MySQL execute"), e), 1, "%s: %s\n<br />%s: %s\n<br/>%s: %s" % (_("Sql function"), str(sqlfunction), _("Sql line"), str(sql_line), _("Values"), str(values)))
            self.__fetchall = self.cursor.fetchall()
        else:
            raise exception.SicolException (_("Database not implemented."),1, "")
            
        

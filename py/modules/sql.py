#!/usr/bin/env python
#-*- coding: utf-8 -*-

#python imports
from os import path
from sys import exit

#project imports
from dom_xml import Xml
from general import General

class Sql( object ):

    g = General()
    root_dir = g.get_config('root_dir')

    mysql = 0
    sqlite = 0

    def __init__( self, dbms ):
        
        self.dbms = dbms
        
        if self.dbms == 'mysql':
            if self.__class__.mysql == 0:
                file = self.g.read_file( path.join( self.root_dir, 'sql', dbms + '.xml' ) )
                self.__class__.mysql = Xml('sql', file)        
        elif self.dbms == 'sqlite':
            if self.__class__.sqlite == 0:
                file = self.g.read_file( path.join( self.root_dir, 'sql', dbms + '.xml' ) )
                self.__class__.sqlite = Xml('sql', file)        
        

    def get(self, sqlfunction):
        
        if self.dbms == 'mysql':
            sql_line = self.__class__.mysql.get(sqlfunction)    
        elif self.dbms == 'sqlite':
            sql_line = self.__class__.sqlite.get(sqlfunction)    
        
        if not sql_line:
            raise KeyError ('sqlfunction "%s" %s.' % (sqlfunction, _("not found in XML file")))
        else: return sql_line
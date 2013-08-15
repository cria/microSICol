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

    def __init__( self, dbms ):
        file = self.g.read_file( path.join( self.root_dir, 'sql', dbms + '.xml' ) )
        self.xml = Xml('sql', file)

    def get(self, sqlfunction):
        sql_line = self.xml.get(sqlfunction)
        if not sql_line:
            raise KeyError ('sqlfunction "%s" %s.' % (sqlfunction, _("not found in XML file")))
        else: return sql_line
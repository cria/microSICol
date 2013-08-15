#!/usr/bin/env python 
#-*- coding: utf-8 -*-

#python imports
from sys import exit

#project imports
from dbconnection import dbConnection
from session import Session
from getdata import Getdata
from lists import Lists
from cgi import FieldStorage

class Subcollections(object):

    coll_html_line = '\t<p id="collection">%s %%s:</p>\n<ul>' % _("Collection")
    subcoll_html_line = '\t\t<li id="subcollection"> <a id="sub_%s_%s" href="./subcollections.py?coll=%s&subcoll=%s">%s</a></li>\n'

    def __init__(self,cookie_value):
        self.form = FieldStorage()
        self.dbconnection = dbConnection()
        self.execute = self.dbconnection.execute
        self.fetch = self.dbconnection.fetch
        self.session = Session()
        self.session.load(cookie_value)
        self.id_user = self.session.data['id_user']
        self.cookie_value = cookie_value

    def list(self):
        '''
        Display all available collections/subcollections which the
        user has access to. Or all of them if he is an Administrator
        @return redirect, html
        '''
        html = ''
        self.execute('get_colls',{'id_user':self.id_user})
        colls = self.fetch('all')
        
        #If logging out and there is only 1 access then logout directly
        if self.form.has_key('logout') and int(self.form.getvalue('logout')) == 1:
            self.execute('get_accesses',{'id_user':self.id_user})
            accesses = self.fetch('one')
            if accesses == 1: #Logout directly
                return True, ''
    
        for coll in colls:
            html += (self.coll_html_line % coll['coll_code'])
            self.execute('get_subcolls',{'id_user':self.id_user,'id_coll':int(coll['id_coll'])})
            subcolls = self.fetch('rows','id_subcoll')
            for id_subcoll in subcolls:
                self.execute('get_subcoll_code',{'id_coll':coll['id_coll'], 'id_subcoll':id_subcoll})
                
                html += (self.subcoll_html_line % (coll['id_coll'], id_subcoll, coll['id_coll'], id_subcoll, self.fetch('one','subcoll_code')))
            html += '\t</ul>\n'
        return False, html

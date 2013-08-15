#!/usr/bin/env python
#-*- coding: utf-8 -*-

import cgitb;cgitb.enable()
#python imports
from sys import exit

#project imports
import exception
from dbconnection import dbConnection
from general import General
from loghelper import Logging

class Login(object):

    def __init__(self, form):
        self.empty_error = False
        self.dbconnection = dbConnection()
        self.execute = self.dbconnection.execute
        self.fetch = self.dbconnection.fetch
        self.g = General()
        self.logger = Logging.getLogger("login")
        self.d = self.logger.debug

        if not (form.has_key("user") and form.has_key("pwd")):
            self.empty_error = True
        else:
            self.user = form.getvalue('user')
            #Transform the user given password to its cryptographed form
            try:
                from hashlib import md5 as new_md5
            except ImportError:
                from md5 import new as new_md5
            self.pwd = new_md5(form.getvalue('pwd')).hexdigest()

    def test( self, cookie_value ):
        if self.empty_error:
            return -1 #Empty error
        else:
            self.execute('login_test',{'login':self.user,'pwd':self.pwd})
            user_exists = self.fetch('columns')
            if (not user_exists['count_login']):
                self.logger.error('Login error: user with password hash %s not found' % self.pwd)
                return -2 #Login Error
            elif (user_exists['count_login'] == 1): #Login Success
                # flag to indicate if subcol page needs to be shown, defaults to True
                show_subcol_page = True

                # get number of subcolls for this user
                self.execute('subcoll_count',{'id_user':user_exists['id_user']})
                number_sub = self.fetch('one', 'subcoll_count')

                # if less than one, raise an exception
                if (number_sub < 1):
                    raise exception.SicolException (_('No subcollections found for this user. Verify table Accesses.'))

                # show this page only when user has more than one subcollection
                if (number_sub < 2):
                    show_subcol_page = False

                # returns 2 if subcoll selection page needs to be shown, 1 otherwise
                if (show_subcol_page):
                    return 2
                else:
                    return 1
            else:
                raise exception.SicolException  ("fetch() %s: %s" % (_('returned invalid code'), str(user_exists)))

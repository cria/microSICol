#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#python imports
from http.cookies import BaseCookie
from os import environ
from time import time, strftime, gmtime

class Cookie(object):

    def __init__(self):
        pass

    def generate(self, code, version='1', path='/', secure='', expires='', comment='cookie_of_session'):
        """Generate coookie hashtable"""
        
        cookie = BaseCookie()
        cookie['Sicol_Session'] = code
        cookie['Sicol_Session']['path'] = path
        if expires:
            cookie['Sicol_Session']['expires'] = expires
        if secure:
            cookie['Sicol_Session']['secure'] = secure
        if comment:
            cookie['Sicol_Session']['comment'] = comment
            
        return cookie

    def send(self, code):
        """Send cookie to browser"""
        cookie = self.generate(code=code)
        return cookie.output()

    def read(self, key):
        """Read value"""

        remote_cookie = BaseCookie(environ.get("HTTP_COOKIE", ""))
        try:
            code = remote_cookie[key].value
        except KeyError:
            return None
        else:
            if code.isalnum():
                return code
            else:
                return None

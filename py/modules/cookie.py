#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#python imports
from Cookie import BaseCookie
from os import environ
from time import time, strftime, gmtime

class Cookie(object):

    def __init__(self):
        pass

    def generate(self, code, version='1', path='/', secure='', expires='', comment='cookie_of_session'):
        """Generate coookie hashtable"""

        config = {}
        config['version'] = version #Integer or Empty. Netscape cookies have version 0. RFC 2965 and RFC 2109 cookies have version 1.
        config['path'] = path
        config['secure'] = secure #True for SSL Conections (https) and Empty for all Conections
        config['expires'] = expires #This format 'Fri,21-May-2006 10:40:51 GMT' or Empty
        config['comment'] = comment #comment from the server explaining the function of this cookie, or None.

        cookie_string = 'Set-Cookie: Sicol_Session=' + code + '; '
        cookie_string += '; '.join([(key + '=' + item) for key, item in config.items()]) + '; '

        return BaseCookie(cookie_string)

    def send(self, code):
        """Send cookie to browser"""
        cookie = self.generate(code=code)
        return cookie

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

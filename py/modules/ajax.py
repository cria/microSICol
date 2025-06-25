#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import cgi
import cgitb; cgitb.enable()
import sys
from .general import General
from .loghelper import Logging
from .json import JsonBuilder

class AjaxBuilder(object):
    g = General()
    http_header = g.get_config('http_header')
    ajax_http_header = g.get_config('ajax_http_header')

    def __init__(self, type = 'html'):
        self.type = type
        self.logger = Logging.getLogger("ajax")
        #self.logger.debug("HTTPHeader: %s" % (self.http_header))

    def get_all_params(self):
        ret = {}
        cgiFields = cgi.FieldStorage()

        for key in cgiFields:
            ret[key] = cgiFields.value

        return ret
    
    def get_params(self, *args, **kwargs):
        ret = []
        for arg in args:
            ret.append(self.get_param(arg))
            
        return ret

    def get_params_dict(self, *args, **kwargs):
        ret = {}
        for arg in args:
            ret[arg] = self.get_param(arg)
            
        return ret

    def get_param(self, param):
        cgiFields = cgi.FieldStorage()
        if param in cgiFields:
            return cgiFields[param].value
        return None
   
    @classmethod
    def parse(cls, jsonString):
        return JsonBuilder.parse(jsonString)
        
    @classmethod
    def dump(cls, obj):
        return JsonBuilder.dump(obj)
        
    def send_response(self, contents):
        if not contents:
            full_page = cgi.test()
        else:
            if (self.type == 'json'):
                full_page = "\n".join((
                        self.http_header + "\n",
                        JsonBuilder.createJson(contents)))
            else:
                full_page = "\n".join((
                        self.http_header + "\n",
                        contents))
                
            full_page = full_page.encode('utf8')
        
        #self.logger.debug("Page: %s" % (full_page.encode('utf8')))
        print(full_page)
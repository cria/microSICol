#!/usr/bin/dev python 
# -*- coding: utf-8 -*-

errors = []

warning_threshold = 0
error_threshold = 1

class Log(object):
    pass
    
class SicolException (Exception):
    """Error catched by the SICOL system"""
    def  __init__ (self, message, level = 1, extras = None):
        global errors
        self.message = message.encode('utf8')
        errors.append ({"message": message,
                        "level": level,
                        "extras": extras})
        self.error_index = len(errors) - 1
        Exception.__init__ (self, message)
        
    def supressErrorMessage():
        global errors
        error = errors[self.error_index]
        del errors[self.error_index]
        return error["message"]
        
    def __str__(self):
        return self.message
    
class SicolSQLException (SicolException):
    def __init__(self, *args, **kwargs):
        SicolException.__init__ (self, *args, **kwargs)

def clear_exceptions():
    global errors
    errors = []
        
def get_html():
    html_warnings = []
    html_errors = []
    for error in errors:
        if error["extras"]:
            extra_html = "<p>%s</p>" % error["extras"]
        else:
            extra_html = ""
        html = """<div class="%%s">%s%s</div>""" % (error["message"], extra_html.replace("%", "%%")) 
        if error["level"] >= error_threshold:
            html_errors.append (html % "error")
        elif error["level"] <= warning_threshold:
            html_warnings.append (html % "warning")
    return "\n".join (html_errors) + "\n".join (html_warnings)


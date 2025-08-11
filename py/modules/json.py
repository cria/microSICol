#!/usr/bin/env python2
#-*- coding: utf-8 -*-

from types import *

class JsonBuilder:
    
    @classmethod
    def createJson(cls, dictionary):
        json = []
        keys = dictionary.keys();
        from loghelper import Logging
        keys.sort();
        
        for key in keys:
            item = dictionary[key]
            format = "'%s': '%s'"

            # if is a dict, recursively add the JSON notation for the dict
            if isinstance(item, dict):
                item = JsonBuilder.createJson(item)
                format = "'%s': %s"

            # TODO
            #if type(item) in (TupleType, ListType):
            #    format = "'%s': %s"
            #    item = "[%s]" % (", ".join(item)) 

            # if type is numeric, use raw value, without scaping
            if type(item) in (IntType, LongType, FloatType):
                format = "'%s': %s"
                
            json.append(format % (key, item))
        
        return "{%s}" % (", ".join(json))
    
    @classmethod
    def parse(cls, jsonString):
        import simplejson
        return simplejson.loads(jsonString)
    
    @classmethod
    def dump(cls, obj):
        import simplejson
        return simplejson.dumps(obj)
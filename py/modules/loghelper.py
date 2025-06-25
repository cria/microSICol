#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

from .general import General
import logging
import pprint

def getLevel(str_level):
    
    log_levels = { 
        'debug' : logging.DEBUG, 
        'info' : logging.INFO, 
        'warn' : logging.WARNING, 
        'warning' : logging.WARNING, 
        'error': logging.ERROR, 
        'critical': logging.CRITICAL }
    
    return log_levels[str_level]
    
class ExtPoint:
    pp = pprint.PrettyPrinter(indent=2)

    def __init__(self, logger):
        self.__subject = logger
        
    def __getattr__( self, name ):
        return getattr( self.__subject, name )

    def debugObj(self, msg, *args, **kwargs):
        args_copy = []
        for arg in args:
            args_copy.append(self.pp.pformat(arg))
            
        self.__subject.debug(msg, *args_copy)

class Logging:
    g = General()
    
    log_filename = g.get_config('log_file')
    log_level = g.get_config('log_level')
    
    if not log_filename:
        log_filename = './sicol.log'
        
    if not log_level:
        log_level = 'error'
    
    file_log = logging.FileHandler(log_filename)
    file_log.setLevel(getLevel(log_level))

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_log.setFormatter(formatter)

    @classmethod
    def getLogger(cls, module, extra = None):
        g = General()
        
        log_name = module
        if extra:
            log_name += '[%s]' % (extra)
        
        logger = logging.getLogger(log_name)
        custom_level = g.get_config('log_level_%s' % module)
        if custom_level:
            logger.setLevel(getLevel(custom_level))
        else:
            logger.setLevel(logging.DEBUG)
            
        logger.addHandler(Logging.file_log)
        return ExtPoint(logger)

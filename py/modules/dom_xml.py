#!/usr/bin/env python 
#-*- coding: utf-8 -*-

#python imports
from os import pardir, sep, path, getcwd
#from dbgp.client import brk

#project imports
from external.BeautifulSoup import BeautifulSoup

class Xml( object ):
        
    def __init__( self, root, file ):        
        tree = BeautifulSoup( file )
        self.tree = tree(root)

    def get( self, name ):
        xml = self.tree
        cdata = ''
        try:
            for i in range( len(xml) ):
                if ( xml[i]['name'] == name ):
                    #if XML content line-breaks
                    if len(xml[i].contents) > 1:
                        cdata =  xml[i].contents[1].decode()
                    else:
                        cdata = xml[i].contents[0].decode()
        except IndexError:
            return ''
        else:
            return cdata ##.encode('utf8')
        
    
    #Returns a dictionary with the first labels serving as keys, and a dictionary as values, containing the internal labels.
    #Josue Andrade 07/06/2011
    def get_dict(self, label, internal_labels):
        #brk(host="localhost", port=9000)
        dict = {}
        tree = self.tree
        for item in tree:
            tmp = {}
            for int_label in internal_labels:                
                if item.has_key(int_label):
                    tmp[int_label] = item[int_label]
            dict[item[label]] = tmp
        
        return dict
        
#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#python imports
from os import pardir, sep, path, getcwd
#from dbgp.client import brk

#project imports
# from .external.BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup


class Xml(object):
    def __init__(self, root, file):
        # Use 'xml' parser for XML files
        self.soup = BeautifulSoup(file, 'xml')
        self.root = self.soup.find(root)

    def get(self, name):
        tag = self.soup.find('config', {'name': name})
        if not tag:
            return ''
        # Retorna o texto da tag (CDATA ou texto comum)
        return tag.get_text(strip=True)

    def get_dict(self, label, internal_labels):
        # Retorna um dicionário com o valor de 'label' como chave e os internos como dict
        result = {}
        if self.root is None:
            return result
        for item in self.root.find_all(label):
            tmp = {}
            for int_label in internal_labels:
                val = item.find(int_label)
                if val is not None:
                    tmp[int_label] = val.get_text(strip=True)
            key = item.get_text(strip=True) if not item.has_attr(label) else item[label]
            result[key] = tmp
        return result

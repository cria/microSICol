#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#python imports
from os import pardir, sep, path, getcwd
#from dbgp.client import brk
import sys
# Garante que o site-packages local está no sys.path
site_packages = '/home/maciel/.local/lib/python3.10/site-packages'
if site_packages not in sys.path:
    sys.path.append(site_packages)

#project imports
# from .external.BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup


class Xml(object):
    def __init__(self, root, file):
        # Use 'xml' parser for XML files
        self.soup = BeautifulSoup(file, 'xml')
        self.root = self.soup.find(root)

    def get(self, name):
        # Busca a tag pelo nome dentro do root
        if self.root is None:
            return ''
        tag = self.root.find(name)
        if tag is None:
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

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#python imports
from os import path
try:
    from hashlib import sha1 as new_sha
except ImportError:
    from sha import new as new_sha

#project imports
from .general import General

class Download(object):

    g = General()
    root_dir = g.get_config('root_dir')
    del g

    def __init__(self, form):

        self.form = form
        self.http_header = '''\
Content-Description: File Transfer
Content-Type: application/octet-stream
Content-Length: %s
Content-Disposition: attachment; filename="%s"\n\n'''

    def doc(self):
        #Set variables
        id = self.form.getvalue('id')
        id_lang = self.form.getvalue('id_lang')
        code = self.form.getvalue('code')
        #Generate file_code
        file_code = str(id) + str(id_lang)
        file_code = new_sha(file_code).hexdigest()

        #Set Document variables
        file_name = self.form.getvalue('file_name_%s' %code)

        doc_dir = path.join(self.root_dir, 'doc_file')
        #Open and Read the File
        try:
            arq = file(path.join(doc_dir, file_code), 'rb')
            data = arq.read()
            arq.close()
        except: data = ''

        header = self.http_header % (len(data), file_name)
        return header + data

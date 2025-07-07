#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#python imports
from time import time
from random import sample
from os import environ, getcwd, path, remove, listdir
from string import ascii_letters, digits
from pickle import dump, load
try:
    from hashlib import sha1 as new_sha
except ImportError:
    from sha import new as new_sha

import os
from os import path
from pickle import dump
#project imports
from .general import General
from .loghelper import Logging

class Session(object):

    g = General()
    root_dir = g.root_dir
    session_dir = g.get_config('session_dir')
    session_path = path.join(root_dir, session_dir)
    extension = g.get_config('session_file_extension')

    def __init__(self):
        #Define Logging
        self.logger = Logging.getLogger("page_mount")
        self.d = self.logger.debug

        from . import config
        try:
          self.timeout = config.session_timeout
        except AttributeError as e:
          self.timeout = 30 * 60 #30 minutes - default value
        self.data = {}

    def create(self):
        #generate and save the session and send the cookie
        self.data['id'] = self.session_id()
        self.data['last_time'] = time()
        self.save()

    def random_string(self,size=10):
        random_string = ''.join(sample(ascii_letters + digits, size))
        return random_string

    def session_id(self):

        #Characteristics of the user for authenticity of cookie
        user_string = str(environ.get('REMOTE_HOST')) + str(environ.get('REMOTE_ADDR')) + str(environ.get('HTTP_USER_AGENT'))

        #Random_string hinders reconstruction of session_string for user
        random_string = self.random_string()

        #Key that will identify the session
        session_string = user_string + str(time()) + random_string

        #Use Secure Hash Algorithm (SHA) to generate a unique ID
        #The SHA is defined by NIST document FIPS PUB 180-2
        #The SHA algorithm is considered a more secure hash.
        session_id = new_sha(session_string.encode('utf8'))
        return session_id.hexdigest()

    def isvalid(self, cookie_value):
        """Determine if the specified session file exists and time expired"""
        if cookie_value:
            if path.exists(path.join(self.session_path, cookie_value+self.extension)):
                return self.load(cookie_value)
            else: return False
        else: return False

    def load(self, session_id, update_last_time=True):
        """Unpickle dictionary of existing session"""
        if session_id:
            try:
                with open(path.join(self.session_path, session_id+self.extension), "rb") as sessionFile:
                        self.data = load(sessionFile)
            except IOError:
                from . import config
                out = config.http_header + '\n\n'
                out += '%s "%s"' % (_("Permission denied to read in"), self.session_path)

            #check whether timeout occurred
            if int(time() - self.data['last_time']) > self.timeout:
                return False
            if update_last_time:
                #update last_time and save
                self.data['last_time'] = time()
                self.save()
            return True

    def save(self):
        """Pickle session dictionary to session file"""
        if self.data['id']:
            try:
                with open(path.join(self.session_path, self.data['id']+self.extension), "wb") as sessionFile:
                    dump(self.data, sessionFile)
            except IOError:
                from . import config
                out = config.http_header + '\n\n'
                out += '%s "%s"' % (_("Permission denied to write in"), self.session_path)
                self.logger.error(out)

    def delete(self, file=None):
        """Delete session file"""
        id = self.data['id']

        if not file:
            file = id + self.extension
        try:
            del self.data
            self.data = {'id':id}
            self.save()
            remove(path.join(self.session_path, file))
        except IOError:
            from . import config
            out = config.http_header + '\n\n'
            out += '%s "%s"' % (_("Permission denied to delete in"), self.session_path)

    def del_expired_sessions(self):
        """Verify which sessions are expired, if true, remove them"""
        directory = listdir(self.session_path)
        for session in directory:
            #Verifies if listed file is really a session file before trying to load it as a session
            if self.extension not in session: continue

            # loads self.data with a dictionary that contents id and last_time
            if not self.load(session.replace(self.extension,''), False):
                # Removing sessions older than allowed timeout
                self.delete(session)


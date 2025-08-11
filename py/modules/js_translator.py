#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#local imports
from os import listdir, path
from general import General
from i18n import code_dict
from session import Session
from dbconnection import dbConnection

class JS_Translator(object):
    g = General()
    js_dir = path.join(g.get_config("root_dir"),g.get_config("js_dir"))
    js_i18n_dir = path.join(g.get_config("root_dir"),g.get_config("js_i18n_dir"))
    
    def __init__(self,cookie_value,i18n,chosen_lang=None):
        '''
        Initialize common class attributes
        '''
        self.i18n = i18n
        self.session = Session()
        self.session.load(cookie_value)
        #Get language code
        self.lang_code = self.get_label_code()
        #Get jsfile
        if chosen_lang is None:
          self.js_file = path.join(self.js_i18n_dir,"translation_%s.js" % self.lang_code)
        else:
          self.js_file = path.join(self.js_i18n_dir,"translation_%s.js" % chosen_lang)
        #Find out which .mo file to look for
        if code_dict.has_key(self.lang_code):
            po_lang_code = code_dict[self.lang_code]
        else:
            po_lang_code = self.lang_code
        self.mo_dir = path.join(self.g.get_config("root_dir"), self.g.get_config("po_dir"), po_lang_code, 'LC_MESSAGES')
        self.mo_file = path.join(self.mo_dir, "sicol.mo")

    def get_label_code(self):
        self.dbconnection = dbConnection()
        self.execute = self.dbconnection.execute
        self.fetch = self.dbconnection.fetch
        lang_code = None
#        if (self.session.data.has_key("id_user")):
#            self.execute('get_user_label',{'id_user':self.session.data['id_user']})
#            lang_code = self.fetch('one')
        if (self.session.data.has_key("label_lang_code")):
            lang_code = self.session.data['label_lang_code']
        if not lang_code:
            lang_code = self.g.get_config('label_lang')
        return lang_code      

    def needsUpdate(self):
        '''
        Checks whether this file needs to be updated or not
        '''
        #Does this file exist?
        if (path.exists(self.js_file) and path.exists(self.mo_file)):
            #Is it up-to-date?
            motime = path.getmtime(self.mo_file)
            jstime = path.getmtime(self.js_file)
            if (motime > jstime):
                return True
            else:
                return False
        else:
            return True

    def doUpdate(self):
        '''
        Get all javascript i18n strings and generate translation array.
        Save array within "translation_<lang-code>.js" file inside /js_i18n/ 
        directory
        '''
        #Get all javascript translatable texts
        js_original = []
        js_translated = {}
        for jsfile in listdir(self.js_dir):
            jsfilepath = path.join(self.js_dir, jsfile)
            if (not path.isdir(jsfilepath)): #it is a file
                if (jsfile.endswith('.js')): #it is a javascript file
                    f = open(jsfilepath,'r')
                    fcontent = f.read()
                    #Get content like: _("text") or _('text')
                    from re import findall, MULTILINE #regular expressions
                    matchobj = findall('_\(["\'](.+?)["\']\)', fcontent, MULTILINE)
                    if (matchobj != [] ):
                        js_original.extend(matchobj)
                    f.close()

        if js_original is not []: #If there is no translatable string then do nothing
            #Get translations
            for original_text in js_original:
                js_translated[original_text] = self.i18n.gettext(original_text).encode('utf-8')

            #Get javascript translation function
            fjavaheader = open(path.join(self.js_i18n_dir, "base_translation.js"), 'r')
            f_jsheader = fjavaheader.read()
            fjavaheader.close()

            #Save javascript translation file
            jscontent = f_jsheader
#            raise str(jscontent + '====' + self.lang_code )
            jscontent += ''.join(["__tr["+`k`+"] = '"+str(v)+"';\n" for k,v in js_translated.iteritems()])
            fjava = open(path.join(self.js_i18n_dir, "translation_"+self.lang_code+".js"), 'w')
            #Add __tinyMCE_lang global variable to set tinyMCE's language
            if code_dict.has_key(self.lang_code):
                tinyMCE_lang = '\nvar __tinyMCE_lang = "' + code_dict[self.lang_code].lower() + '";\n'
            else:
                tinyMCE_lang = '\nvar __tinyMCE_lang = "' + self.lang_code.lower() + '";\n'
            jscontent += tinyMCE_lang
            fjava.write(jscontent)
            fjava.close()

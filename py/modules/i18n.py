#!/usr/bin/env python 
#-*- coding: utf-8 -*-

#project imports
from general import General

#fill in the dictionary bellow if your posix locale language code
#differs from the iso code used in the database:
code_dict = {
             'ptbr': 'pt_BR',
            }

class I18n(object):
    g = General()

    def __init__(self, lang_code=None, cookie_value=None):
        #Verify and compose lang_code
        if not lang_code:
            if not cookie_value:
                lang_code = self.g.get_config('label_lang')
            else:
                from session import Session
                session = Session()
                try:
                    session.load(cookie_value)
                    if (session.data.has_key('label_lang_code')):
                        lang_code = session.data['label_lang_code']
                    else:
                        lang_code = self.g.get_config('label_lang')
                except:
                    lang_code = self.g.get_config("label_lang")
        if (len(lang_code) < 2) or (len(lang_code) > 4) or (not lang_code):
            lang_code = 'en'

        #If needed, convert lang_code to posix locale code
        if code_dict.has_key(lang_code):
            lang_code = code_dict[lang_code]

        #Install lang
        from os import path
        self.locale_dir = path.join(self.g.get_config('root_dir'), self.g.get_config('po_dir'))
        self.language_install(lang_code)

    def language_install (self, lang_code):
        try:
            from gettext import translation
            self.lang = translation ('sicol', self.locale_dir, languages=[lang_code, 'en'])
            self.lang.install()
            _ = self.gettext
            #self.gettext = _ = lang.ugettext
        #if lang does not exist, bind _ to a do nothing function
        except IOError:
            _ = lambda x: x
        import __builtin__
        __builtin__.__dict__['_'] = _

    def gettext(self,text):
        '''
        Format translated data in order to avoid
        Unicode(De|En)codeErrors
        '''
        try:
          tr_text = str(self.lang.ugettext(text))
        except UnicodeEncodeError:
          try:
            tr_text = str(self.lang.ugettext(text).encode('utf8'))
          except UnicodeEncodeError:
            tr_text = str(self.lang.ugettext(text).decode('utf8'))
        return tr_text.decode('utf8')

    def set_lang(self, lang_code):
        if code_dict.has_key(lang_code):
            lang_code = code_dict[lang_code]
        self.language_install(lang_code)

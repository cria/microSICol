#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#project imports
from enum import Enum
from dbconnection import dbConnection
from urllib import urlencode

class Keyword(Enum):
    #Enumerate keywords
    NONE, REF, DOC, LINK, TAX = range(5)

class TextLink(object):
    """One Standard TextLink"""

    def __init__(self, keyword=Keyword.NONE, hyperlink=""):

        #Define property
        self.__keyword = Keyword.NONE
        self.__hyperlink = "<a href='#'>" + _("Invalid Text Link") + "</a>"

        #Fill property
        self.keyword = keyword
        if hyperlink != "":
            self.hyperlink = hyperlink

    ####################
    # Property keyword #
    ####################

    #getter and setter of keyword
    def get_keyword(self):
        return self.__keyword

    def set_keyword(self, value):

        #str and unicode inherit basestring
        if isinstance(value, basestring):
            if TextLink.isValidKeyword(value):
                self.__keyword = TextLink.ToKeyword(value.strip())
            else:
                self.__keyword = Keyword.NONE

        elif isinstance(value, type(Keyword)):
            self.__keyword = value

        else:
            raise TypeError, _("Invalid Keyword type.")

    #Define keyword property
    keyword = property(get_keyword, set_keyword)

    ######################
    # Property hyperlink #
    ######################

    #getter and setter of hyperlink
    def get_hyperlink(self):
        return self.__hyperlink

    def set_hyperlink(self, value):
        if value.find("<a") == 0 and value.find(">", 2, len(value) - 4 ) and value.find("</a>") == len(value) - 4:
            self.__hyperlink = value
        else:
            raise ValueError, _("Invalid Hyperlink type.")

    #Define hyperlink property
    hyperlink = property(get_hyperlink, set_hyperlink)

    ######################
    # Overridden Methods #
    ######################

    def __str__(self):
        return str(self.keyword) + ":" + self.hyperlink

    def __cmp__(self, other):
        return cmp(str(self), str(other))

    def __repr__(self):
        return str(self)

    #################
    # Class Methods #
    #################

    @classmethod
    def isStandardTextLink(cls, text):
        """Verify text is a Standard TextLink"""

        tlink = text.split(":")

        #Validation
        if len(tlink) == 2 and TextLink.isValidKeyword(tlink[0].strip()):
            return True
        else:
            return False

    @classmethod
    def isValidKeyword(cls, keyword):
        """Verify text is valid Keyword of TextLink"""

        #Validation
        if keyword.strip().upper() == str(Keyword.REF):
            return True
        elif keyword.strip().upper() == str(Keyword.DOC):
            return True
        elif keyword.strip().upper() == str(Keyword.LINK):
            return True
        elif keyword.strip().upper() == str(Keyword.TAX):
            return True
        else:
            return False

    @classmethod
    def ToKeyword(cls, sKey):
        """Convert text and return a valid Keyword type.
           If text is not valid Keyword, raise a exception."""

        if sKey.strip().upper() == str(Keyword.REF):
            return Keyword.REF
        elif sKey.strip().upper() == str(Keyword.DOC):
            return Keyword.DOC
        elif sKey.strip().upper() == str(Keyword.LINK):
            return Keyword.LINK
        elif sKey.strip().upper() == str(Keyword.TAX):
            return Keyword.TAX
        else:
           raise ValueError, _("Cannot be convert to Keyword.")

    @classmethod
    def ToHyperLink(cls, keyword, text, cookie_value, id_lang=0):
        """Convert text and return a hyperlink.
           Optional: id_lang is mandatory to keyword 'DOC' AND keyword 'REF'"""

        #Define Database
        cls.__dbConnection = dbConnection(cookie_value)

        #"str" and "unicode" inherit "basestring"
        #If keyword type is basestring, convert to Keyword TextLink
        if isinstance(keyword, basestring):
            try:
                keyword = TextLink.ToKeyword(keyword)
            except:
                keyword = Keyword.NONE

        if keyword == Keyword.REF:
            try:
                strName = ""
                strHref = ""
                strDesc = ""
                strTitle = ""
                try:
                    strName = "ref%s" % text.strip()                    
                    cls.__dbConnection.execute('get_ref_title', {'id_ref':text.strip(), 'id_coll':cls.__dbConnection.session.data['id_coll']})
                    rowref = cls.__dbConnection.fetch('columns')
                    if(len(rowref) > 1):
                        strDesc = rowref['title']
                        strTitle = rowref['title']
                        strHref = "./refpopup.detail.py?%s" % (urlencode({'id':rowref['id_ref']}))
                    else:
                        raise Exception, _("Error in database.")
                except:
                    strName = "ref%s" % text.strip()
                    strHref = "#"
                    strDesc = _("Invalid TextLink")
                    strTitle = "[%s:%s]" % (str(keyword), text.strip())
            finally:
                return """<a title='%s' href='javascript:popWinOpen("%s",760,400,"%s");' class=\"tlink\" name='%s'>%s</a>""" % (strTitle, strHref, _("Reference Visualization"), strName, strDesc )

        elif keyword == Keyword.DOC:
            try:
                strName = ""
                strHref = ""
                strDesc = ""
                strTitle = ""
                try:
                    strName = "doc%s" % text.strip()
                    cls.__dbConnection.execute('get_doc_title', {'code':str(text).strip(), 'id_lang':id_lang, 'id_coll':cls.__dbConnection.session.data['id_coll']})
                    rowdoc = cls.__dbConnection.fetch('columns')
                    if(len(rowdoc) > 1):
                        strDesc = rowdoc['title']
                        strTitle = rowdoc['title']
                        strHref = "./docpopup.detail.py?%s" % (urlencode({'id':rowdoc['id_doc']}))
                    else:
                        raise Exception, "Error in database."
                except:
                    strName = "doc%s" % text.strip()
                    strHref = "#"
                    strDesc = _("Invalid TextLink")
                    strTitle = "[%s:%s]" % (str(keyword), text.strip())
            finally:
                return """<a title='%s' href='javascript:popWinOpen("%s",760,400,"%s");' class=\"tlink\" name='%s'>%s</a>""" % (strTitle, strHref, _("Document Visualization"), strName, strDesc)

        elif keyword == Keyword.TAX:
            try:
                #Get each one of the names
                counter = 1;
                sp_dict = {}
                sp_dict['first'] = ''
                sp_dict['second'] = ''
                sp_dict['third'] = ''
                sp_dict['lang'] = cls.__dbConnection.session.data['label_lang_code'][:2]
                strNames = text.split(" ")
                strFormat = []
                isFirst = True
                for strName in strNames:
                    if not isFirst and strName[-1] == ".": #disable special format 
                        strFormat.append("<span class='notaxaformat'>"+strName+"</span>")
                    else: 
                        strFormat.append("<span class='taxaformat'>"+strName+"</span>")
                    isFirst = False
                    #Build dictionary link
                    if counter == 1:
                        sp_dict['first'] = strName
                    elif counter == 2:
                        sp_dict['second'] = strName
                    elif counter == 3:
                        sp_dict['third'] = strName
                    counter += 1
                external_dict_link = "href='http://names.cria.org.br/index?genus=%(first)s&species=%(second)s&subspecies=%(third)s&lang=%(lang)s'" % sp_dict
                strFormat = " ".join(strFormat)
            finally:
                return "<a target='_blank' %s><img src='../img/sp.png' /> %s</a>" % (external_dict_link,strFormat)
        elif keyword == Keyword.LINK:            
            try:
                strName = ""
                strHref = ""
                strDesc = ""
                strTitle = ""
                try:                    
                    NameAndHref = text.strip().split('|')
                    if len(NameAndHref) == 2:
                        if NameAndHref[1] == '':
                            strName = "link%s" % (NameAndHref[0].strip())
                            strDesc = NameAndHref[0].strip()
                            strTitle = NameAndHref[0].strip()
                            strHref = "http://%s" % (NameAndHref[0].strip())
                        else:
                            strName = "link%s" % (NameAndHref[1].strip())
                            strDesc = NameAndHref[0].strip()
                            strTitle = NameAndHref[0].strip()
                            strHref = "http://%s" % (NameAndHref[1].strip())
                    elif len(NameAndHref) == 1:
                        strName = "link%s" % (NameAndHref[0].strip())
                        strDesc = NameAndHref[0].strip()
                        strTitle = NameAndHref[0].strip()
                        strHref = "http://%s" % (NameAndHref[0].strip())
                    else:
                        raise Exception, "Error in database."
                except:
                    strName = "link%s" % (text.strip())
                    strHref = "#"
                    strDesc = _("Invalid TextLink")
                    strTitle = "[%s:%s]" % (str(keyword), text.strip())
            finally:
                return """<a target='_blank' title='%s' href='%s' class="tlink" name='%s'>%s</a>""" % (strTitle, strHref, strName, strDesc)
        else:
            strName = "[" + str(keyword) + ":" + text.strip() + "]"
            strHref = "#"
            strDesc = _("Invalid TextLink")
            strTitle = "[" + str(keyword) + ":" + text.strip() + "]"

            return """<a title='%s' href='%s' class="tlink" name='%s'>%s</a>""" % (strTitle, strHref, strName, strDesc)

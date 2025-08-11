#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#project imports
from textlinkcollection import TextLinkCollection
from textlink import TextLink
from textlink import Keyword
from session import Session

class TextLinkFactory(dict):
    """Factory for TextLink and TextLinkCollection manipulation."""

    def __init__(self, cookie_value, session_lang=0, data_lang=0):
        """session_lang is used only for keyword 'DOC'.
           data_lang is used only for keyword 'REF'."""

        self.__cookie = cookie_value

        self.session_lang = session_lang
        self.data_lang = data_lang

        dict.__init__(self)

    ######################
    # Overridden Methods #
    ######################

    def __setitem__(self, key, value):

        #str and unicode inherit basestring
        if isinstance(value, basestring):
            dict.__setitem__(self, key, self.replaceWithHyperLinks(value))

        elif isinstance(value, TextLink):
            dict.__setitem__(self, key, value.hyperlink)

        elif isinstance(value, TextLinkCollection):
            dict.__setitem__(self, key, self.extractHyperLinks(value))

        else:
            raise TypeError, _("Invalid value type.")

    def update(self, e={}, **f):
        try:
            if len(e) != 0:
                for key, value in e.items():

                    #"str" and "unicode" inherit "basestring"
                    if isinstance(value, basestring):
                        e[key] = self.replaceWithHyperLinks(value)

                    elif isinstance(value, TextLink):
                        e[key] = value.hyperlink

                    elif isinstance(value, TextLinkCollection):
                        e[key] = self.extractHyperLinks(value)

                    else:
                        raise TypeError, _("Invalid value type.")

            if len(f) != 0:
                for key, value in f.items():

                    #"str" and "unicode" inherit "basestring"
                    if isinstance(value, basestring):
                        f[key] = self.replaceWithHyperLinks(value)

                    elif isinstance(value, TextLink):
                        f[key] = value.hyperlink

                    elif isinstance(value, TextLinkCollection):
                        f[key] = self.extractHyperLinks(value)

                    else:
                        raise TypeError, _("Invalid value type.")

            dict.update(self, e, **f)
        except:
            raise

    ##################
    # Object Methods #
    ##################

    #Extract all TextLinks from text
    def extractTextLinks(self, text, mode="e"):
        """Extract all TextLinks from text and return TextLinkCollection.
           Optional: mode='e' (Extract) or mode='r' (Mark for replace). Default is 'e'."""

        tlinks = TextLinkCollection()

        searching = True
        start = text.find("[")
        end = text.find("]")

        #Copy original to replace text while searching
        if mode =="r":
            replacedtext = text

        #Search all text links
        while searching:
            if start < end:
                if TextLink.isStandardTextLink(text[start+1:end]):
                    try:
                        tlinks.append(self.convertToTextLink(text[start+1:end]))
                        if mode == "r":
                            replacedtext = replacedtext.replace(text[start:end+1], "%s", 1)
                    finally:
                        pass
                if end == len(text):
                    searching = False
                else:
                    start = text.find("[", start + 1)
                    end = text.find("]", start + 2)
                    if start == -1 or end == -1:
                        searching = False
            else:
                if start == -1 or end == -1:
                    searching = False
                else:
                    end = text.find("]", start + 2)
                    if end == -1:
                        searching = False

        if mode == 'r':
            return tlinks, replacedtext
        else:
            return tlinks

    #Replace all TextLinks from text
    def replaceWithHyperLinks(self, text):
        """Replace text with TextLinks' HyperLinks in text"""

        #Fill TextLinks and text replaced with %s
        tlinks, replacedtext = self.extractTextLinks(text, 'r')

        #Get hyperlinks and return
        return replacedtext % tuple([item.hyperlink for item in tlinks])

    #Extract Hyperlinks and returns a object str type
    def extractHyperLinks(self, tlinkcoll):
        if isinstance(tlinkcoll, TextLinkCollection):
            for item in tlinkcoll:
                text += item.split(":")[1] + " "
            return text
        else:
            raise TypeError, _("Invalid value type.")

    #Fill data object
    def fillData(self, data):
        """Fill in data with TextLinks' HyperLinks saved in associated keys"""

        for key, value in self.items():
            data[key] = value

    #Convert str type to TextLink type
    def convertToTextLink(self, text):
        if TextLink.isStandardTextLink(text):
            keyword = TextLink.ToKeyword(text.split(":")[0].strip())
            if keyword == Keyword.DOC:
                hyperlink = TextLink.ToHyperLink(keyword, text.split(":")[1].strip(), self.__cookie, self.session_lang)
            elif keyword == Keyword.REF:
                hyperlink = TextLink.ToHyperLink(keyword, text.split(":")[1].strip(), self.__cookie, self.data_lang)
            else:
                hyperlink = TextLink.ToHyperLink(keyword, text.split(":")[1].strip(), self.__cookie)

            #Return a TextLink
            return TextLink(keyword, hyperlink)
        else:
            raise ValueError, _("Cannot be converted to TextLink type.")

    #Convert list type to TextLinkCollection type
    def convertToTextLinkCollection(self, tlist):
        listItems = list()

        #Transform value in standard TextLinks and create list
        for item in tlist:
            if isinstance(item, TextLink):
                listItems.append(item)
            elif isinstance(item, basestring):
                if isinstance(self.__cookie, str):
                    tlinkFactory = TextLinkFactory(self.__cookie)
                    listItems.append(tlinkFactory.convertToTextLink(item))
                else:
                    raise Exception("The cookie_value is mandatory to str type values")
            else:
                raise TypeError, _("Invalid value type in list.")

        #Return list
        return listItems

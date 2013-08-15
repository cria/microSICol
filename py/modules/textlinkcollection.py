#!/usr/bin/env python 
#-*- coding: utf-8 -*-

#project imports
from textlink import TextLink

class TextLinkCollection(list):
    """Collection of Standard TextLinks"""

    def __init__(self):
        list.__init__(self)

    ######################
    # Overridden Methods #
    ######################

    def __setitem__(self, index, value):
        if isinstance(value, TextLink):
            list.__setitem__(self, index, value)

        elif isinstance(value, TextLinkCollection):
            try:

                #Transform index int to index slice
                if not isinstance(index, slice):
                    index = slice(index, index + 1)

                #Save TextLinks
                list.__setitem__(self, index, value)
            except:
                raise

        else:
            raise TypeError, _("Invalid value type.") 

    def __setslice__(self, index, indexf, value):
        if isinstance(value, TextLink):
            list.__setslice__(self, index, indexf, value)

        elif isinstance(value, TextLinkCollection):
            list.__setslice__(self, index, indexf, listItems)

        else:
            raise TypeError, _("Invalid value type.") 

    def __str__(self):
        text = []
        for item in self:
            text.append("%s:%s" % (str(item.keyword),item.hyperlink.encode('utf-8')))
        return "|".join(text)

    def __repr__(self):
        return str(self)

    def append(self, value):
        if isinstance(value, TextLink):
            list.append(self, value)

        elif isinstance(value, TextLinkCollection):
            list.extend(self, value)

        else:
            raise TypeError, _("Invalid value type.") 

    def extend(self, value):
        if isinstance(value, TextLink):
            list.extend(self, value)

        elif isinstance(value, TextLinkCollection):
            list.extend(self, value)

        else:
            raise TypeError, _("Invalid value type.") 

    def insert(self, index, value):
        if isinstance(value, TextLink):
            list.insert(self, index, value)

        elif isinstance(value, TextLinkCollection):
            cont = index
            for item in value:
                list.insert(self, cont, value)
                cont += 1

        else:
            raise TypeError, _("Invalid value type.") 

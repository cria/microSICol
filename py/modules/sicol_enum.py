#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

import string

class EnumMetaClass:
    """Metaclass for enumeration.

    To define your own enumeration, do something like

    class Color(Enum):
        red = 1
        green = 2
        blue = 3

    Now, Color.red, Color.green and Color.blue behave totally
    different: they are enumerated values, not integers.

    Enumerations cannot be instantiated; however they can be
    subclassed.

    """

    def __init__(self, name, bases, dict):
        """Constructor -- create an enumeration.

        Called at the end of the class statement.  The arguments are
        the name of the new class, a tuple containing the base
        classes, and a dictionary containing everything that was
        entered in the class' namespace during execution of the class
        statement.  In the above example, it would be {'red': 1,
        'green': 2, 'blue': 3}.

        """
        for base in bases:
            if base.__class__ is not EnumMetaClass:
                raise TypeError("Enumeration base class must be enumeration")
        bases = [x for x in bases if x is not Enum]
        self.__name__ = name
        self.__bases__ = bases
        self.__dict = {}
        for key, value in list(dict.items()):
            self.__dict[key] = EnumInstance(name, key, value)

    def __getattr__(self, name):
        """Return an enumeration value.

        For example, Color.red returns the value corresponding to red.

        This looks in the class dictionary and if it is not found
        there asks the base classes.

        The special attribute __members__ returns the list of names
        defined in this class (it does not merge in the names defined
        in base classes).

        """
        if name == '__members__':
            return list(self.__dict.keys())

        try:
            return self.__dict[name]
        except KeyError:
            for base in self.__bases__:
                try:
                    return getattr(base, name)
                except AttributeError:
                    continue

        raise AttributeError(name)

    def __repr__(self):
        s = self.__name__
        if self.__bases__:
            s = s + '(' + string.join([x.__name__ for x in self.__bases__], ", ") + ')'
        if self.__dict:
            list = []
            for key, value in list(self.__dict.items()):
                list.append("%s: %s" % (key, int(value)))
            s = "%s: {%s}" % (s, string.join(list, ", "))
        return s


class EnumInstance:
    """Class to represent an enumeration value.

    EnumInstance('Color', 'red', 12) prints as 'Color.red' and behaves
    like the integer 12 when compared, but doesn't support arithmetic.

    """

    def __init__(self, classname, enumname, value):
        self.__classname = classname
        self.__enumname = enumname
        self.__value = value

    def __int__(self):
        return self.__value

    def __str__(self):
        return self.__enumname

    def __repr__(self):
        return "%s.%s int(%s)" % (self.__classname, self.__enumname, self.__value)

    def __cmp__(self, other):
        if isinstance(other, EnumInstance):
            return cmp(self.__value, int(other))
        else:
            raise TypeError("Invalid type to compare.")

# Create the base class for enumerations.
# It is an empty enumeration.
Enum = EnumMetaClass("Enum", (), {})
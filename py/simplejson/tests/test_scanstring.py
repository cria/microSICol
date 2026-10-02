#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import sys
import decimal
from unittest import TestCase

import simplejson.decoder

class TestScanString(TestCase):
    def test_py_scanstring(self):
        self._test_scanstring(simplejson.decoder.py_scanstring)

    def test_c_scanstring(self):
        if not simplejson.decoder.c_scanstring:
            return
        self._test_scanstring(simplejson.decoder.c_scanstring)

    def _test_scanstring(self, scanstring):
        self.assertEqual(
            scanstring('"z\\ud834\\udd20x"', 1, None, True),
            ('z\U0001d120x', 16))

        if sys.maxunicode == 65535:
            self.assertEqual(
                scanstring('"z\U0001d120x"', 1, None, True),
                ('z\U0001d120x', 6))
        else:
            self.assertEqual(
                scanstring('"z\U0001d120x"', 1, None, True),
                ('z\U0001d120x', 5))

        self.assertEqual(
            scanstring('"\\u007b"', 1, None, True),
            ('{', 8))

        self.assertEqual(
            scanstring('"A JSON payload should be an object or array, not a string."', 1, None, True),
            ('A JSON payload should be an object or array, not a string.', 60))
        
        self.assertEqual(
            scanstring('["Unclosed array"', 2, None, True),
            ('Unclosed array', 17))
        
        self.assertEqual(
            scanstring('["extra comma",]', 2, None, True),
            ('extra comma', 14))
        
        self.assertEqual(
            scanstring('["double extra comma",,]', 2, None, True),
            ('double extra comma', 21))
        
        self.assertEqual(
            scanstring('["Comma after the close"],', 2, None, True),
            ('Comma after the close', 24))
        
        self.assertEqual(
            scanstring('["Extra close"]]', 2, None, True),
            ('Extra close', 14))
        
        self.assertEqual(
            scanstring('{"Extra comma": true,}', 2, None, True),
            ('Extra comma', 14))
        
        self.assertEqual(
            scanstring('{"Extra value after close": true} "misplaced quoted value"', 2, None, True),
            ('Extra value after close', 26))
        
        self.assertEqual(
            scanstring('{"Illegal expression": 1 + 2}', 2, None, True),
            ('Illegal expression', 21))
        
        self.assertEqual(
            scanstring('{"Illegal invocation": alert()}', 2, None, True),
            ('Illegal invocation', 21))
        
        self.assertEqual(
            scanstring('{"Numbers cannot have leading zeroes": 013}', 2, None, True),
            ('Numbers cannot have leading zeroes', 37))
        
        self.assertEqual(
            scanstring('{"Numbers cannot be hex": 0x14}', 2, None, True),
            ('Numbers cannot be hex', 24))
        
        self.assertEqual(
            scanstring('[[[[[[[[[[[[[[[[[[[["Too deep"]]]]]]]]]]]]]]]]]]]]', 21, None, True),
            ('Too deep', 30))
        
        self.assertEqual(
            scanstring('{"Missing colon" null}', 2, None, True),
            ('Missing colon', 16))
        
        self.assertEqual(
            scanstring('{"Double colon":: null}', 2, None, True),
            ('Double colon', 15))
        
        self.assertEqual(
            scanstring('{"Comma instead of colon", null}', 2, None, True),
            ('Comma instead of colon', 25))
        
        self.assertEqual(
            scanstring('["Colon instead of comma": false]', 2, None, True),
            ('Colon instead of comma', 25))
        
        self.assertEqual(
            scanstring('["Bad value", truth]', 2, None, True),
            ('Bad value', 12))

#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

from unittest import TestCase

import simplejson as S

class TestUnicode(TestCase):
    def test_encoding1(self):
        encoder = S.JSONEncoder(encoding='utf-8')
        u = '\N{GREEK SMALL LETTER ALPHA}\N{GREEK CAPITAL LETTER OMEGA}'
        s = u.encode('utf-8')
        ju = encoder.encode(u)
        js = encoder.encode(s)
        self.assertEqual(ju, js)
    
    def test_encoding2(self):
        u = '\N{GREEK SMALL LETTER ALPHA}\N{GREEK CAPITAL LETTER OMEGA}'
        s = u.encode('utf-8')
        ju = S.dumps(u, encoding='utf-8')
        js = S.dumps(s, encoding='utf-8')
        self.assertEqual(ju, js)

    def test_encoding3(self):
        u = '\N{GREEK SMALL LETTER ALPHA}\N{GREEK CAPITAL LETTER OMEGA}'
        j = S.dumps(u)
        self.assertEqual(j, '"\\u03b1\\u03a9"')

    def test_encoding4(self):
        u = '\N{GREEK SMALL LETTER ALPHA}\N{GREEK CAPITAL LETTER OMEGA}'
        j = S.dumps([u])
        self.assertEqual(j, '["\\u03b1\\u03a9"]')

    def test_encoding5(self):
        u = '\N{GREEK SMALL LETTER ALPHA}\N{GREEK CAPITAL LETTER OMEGA}'
        j = S.dumps(u, ensure_ascii=False)
        self.assertEqual(j, '"%s"' % (u,))

    def test_encoding6(self):
        u = '\N{GREEK SMALL LETTER ALPHA}\N{GREEK CAPITAL LETTER OMEGA}'
        j = S.dumps([u], ensure_ascii=False)
        self.assertEqual(j, '["%s"]' % (u,))

    def test_big_unicode_encode(self):
        u = '\U0001d120'
        self.assertEqual(S.dumps(u), '"\\ud834\\udd20"')
        self.assertEqual(S.dumps(u, ensure_ascii=False), '"\U0001d120"')

    def test_big_unicode_decode(self):
        u = 'z\U0001d120x'
        self.assertEqual(S.loads('"' + u + '"'), u)
        self.assertEqual(S.loads('"z\\ud834\\udd20x"'), u)

    def test_unicode_decode(self):
        for i in range(0, 0xd7ff):
            u = chr(i)
            json = '"\\u%04x"' % (i,)
            self.assertEqual(S.loads(json), u)
    
    def test_default_encoding(self):
        self.assertEqual(S.loads('{"a": "\xe9"}'.encode('utf-8')),
            {'a': '\xe9'})

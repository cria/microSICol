#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

from unittest import TestCase
import simplejson as S

# from http://json.org/JSON_checker/test/pass2.json
JSON = r'''
[[[[[[[[[[[[[[[[[[["Not too deep"]]]]]]]]]]]]]]]]]]]
'''

class TestPass2(TestCase):
    def test_parse(self):
        # test in/out equivalence and parsing
        res = S.loads(JSON)
        out = S.dumps(res)
        self.assertEqual(res, S.loads(out))

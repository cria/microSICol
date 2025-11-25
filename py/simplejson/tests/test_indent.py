#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

from unittest import TestCase

import simplejson as S
import textwrap

class TestIndent(TestCase):
    def test_indent(self):
        h = [['blorpie'], ['whoops'], [], 'd-shtaeou', 'd-nthiouh', 'i-vhbjkhnth',
             {'nifty': 87}, {'field': 'yes', 'morefield': False} ]

        expect = textwrap.dedent("""\
        [
          [
            "blorpie"
          ],
          [
            "whoops"
          ],
          [],
          "d-shtaeou",
          "d-nthiouh",
          "i-vhbjkhnth",
          {
            "nifty": 87
          },
          {
            "field": "yes",
            "morefield": false
          }
        ]""")


        d1 = S.dumps(h)
        d2 = S.dumps(h, indent=2, sort_keys=True, separators=(',', ': '))

        h1 = S.loads(d1)
        h2 = S.loads(d2)

        self.assertEqual(h1, h)
        self.assertEqual(h2, h)
        self.assertEqual(d2, expect)

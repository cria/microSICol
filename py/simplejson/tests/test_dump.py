#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

from unittest import TestCase
from io import StringIO

import simplejson as S

class TestDump(TestCase):
    def test_dump(self):
        sio = StringIO()
        S.dump({}, sio)
        self.assertEqual(sio.getvalue(), '{}')
    
    def test_dumps(self):
        self.assertEqual(S.dumps({}), '{}')

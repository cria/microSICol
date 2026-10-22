#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

from unittest import TestCase

import simplejson as S

class TestDefault(TestCase):
    def test_default(self):
        self.assertEqual(
            S.dumps(type, default=repr),
            S.dumps(repr(type)))

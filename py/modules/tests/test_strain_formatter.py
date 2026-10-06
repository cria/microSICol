#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from mock import Mock, patch
import unittest

from strain_formatter import StrainFormatter, StrainFormatterError


class StrainFormatterTestCase(unittest.TestCase):
    def setUp(self):
        super(StrainFormatterTestCase, self).setUp()

        self.dbConnection_patcher = patch('strain_formatter.dbConnection')
        self.dbConnection_patcher.start()

        self.s = StrainFormatter()

    def testValidPatternsReturnsTrue(self):
        self.assertTrue(self.s.check_pattern('CBMAI ####'))

    def testInvalidPatternsRaisesException(self):
        self.assertRaises(StrainFormatterError, self.s.check_pattern, 'CBMAI')

    def testValidConvertToUsualPatternOk(self):
        self.assertEqual(self.s.convert_to_usual_pattern('CBMAI ####'), 'CBMAI %04d')

    def testInvalidConvertToUsualPatternRaisesException(self):
        self.assertRaises(StrainFormatterError, self.s.convert_to_usual_pattern, 'CBMAI')

    def testValidFormatStrainCodeWithPatternOk(self):
        self.assertEqual(self.s.format_strain_code_with_pattern(32, 'CB #### MAI'), 'CB 0032 MAI')
        self.assertEqual(self.s.format_strain_code_with_pattern(21, 'CB A#### MAI'), 'CB A0021 MAI')
        self.assertEqual(self.s.format_strain_code_with_pattern('21', 'CB A#### MAI'), 'CB A0021 MAI')

    def testValidFormatStrainCodeWithDivisionOk(self):
        self.s.get_division_pattern = Mock()
        self.s.get_division_pattern.return_value = 'CBMAI ####'

        numeric_code = 32
        id_division = 1
        self.assertEqual(self.s.format_strain_code_with_division(numeric_code, id_division), 'CBMAI 0032')
        self.assertTrue(self.s.get_division_pattern.called)
        self.s.get_division_pattern.assert_called_with(id_division)

        self.s.get_division_pattern.reset_mock()
        self.s.get_division_pattern.return_value = 'CBMAI A####'

        numeric_code = 21
        id_division = 2
        self.assertEqual(self.s.format_strain_code_with_division(numeric_code, id_division), 'CBMAI A0021')
        self.assertTrue(self.s.get_division_pattern.called)
        self.s.get_division_pattern.assert_called_with(id_division)

    def testInvalidFormatStrainCodeWithDivisionRaises(self):
        self.s.get_division_pattern = Mock()
        self.s.get_division_pattern.return_value = 'CBMAI ####'

        self.assertRaises(StrainFormatterError, self.s.format_strain_code_with_division, '', id_division=1)
        self.assertRaises(StrainFormatterError, self.s.format_strain_code_with_division, None, id_division=1)

    def testValidGetDivisionPatternOk(self):
        self.s.fetch.return_value = 'CBMAI ####'

        id_division = 1
        self.assertEqual(self.s.get_division_pattern(id_division), 'CBMAI ####')
        self.assertTrue(self.s.execute.called)
        self.s.execute.assert_called_with('get_division_pattern',
                                          {'id_division': id_division})
        self.assertTrue(self.s.fetch.called)
        self.s.fetch.assert_called_with('one')

    def testInvalidGetDivisionPatternRaisesException(self):
        self.s.fetch.return_value = ''

        id_division = 99
        self.assertRaises(StrainFormatterError, self.s.get_division_pattern, id_division)
        self.assertTrue(self.s.execute.called)
        self.s.execute.assert_called_with('get_division_pattern',
                                          {'id_division': id_division})
        self.assertTrue(self.s.fetch.called)
        self.s.fetch.assert_called_with('one')

    def testGetValidDivisionListOk(self):
        self.s.fetch.return_value = [
            {'id_division': 1, 'division': 'DEFAULT', 'pattern': 'CBMAI ####', },
            {'id_division': 2, 'division': 'ANT', 'pattern': 'CBMAI A####', },
            {'id_division': 3, 'division': 'SEA', 'pattern': 'CBMAI ####-S', },
        ]

        expected_dict = (
            {'id_division': 1, 'division': 'DEFAULT', 'pattern': 'CBMAI ####', },
            {'id_division': 2, 'division': 'ANT', 'pattern': 'CBMAI A####', },
            {'id_division': 3, 'division': 'SEA', 'pattern': 'CBMAI ####-S', },
        )

        id_subcoll = 1
        self.assertEqual(self.s.get_division_list(id_subcoll), expected_dict)
        self.assertTrue(self.s.execute.called)
        self.s.execute.assert_called_with('get_division_list',
                                          {'id_subcoll': id_subcoll})

        self.assertTrue(self.s.fetch.called)
        self.s.fetch.assert_called_with('all')

    def testGetInvalidDivisionListEmptyTuple(self):
        self.s.fetch.return_value = []

        expected_tuple = tuple()

        id_subcoll = 99
        self.assertEqual(self.s.get_division_list(id_subcoll), expected_tuple)
        self.assertTrue(self.s.execute.called)
        self.s.execute.assert_called_with('get_division_list',
                                          {'id_subcoll': id_subcoll})

        self.assertTrue(self.s.fetch.called)
        self.s.fetch.assert_called_with('all')

    def testValidUpdateDivisionPattern3(self):
        self.s.fetch.return_value = [
            {'numeric_code': 10, 'id_strain': 1},
            {'numeric_code': 20, 'id_strain': 2},
            {'numeric_code': 30, 'id_strain': 3},
        ]

        qtd_strains = 3
        self.assertEqual(self.s.update_division_pattern(1, 'DEFAULT', 'CB ### MAI'), qtd_strains)

        self.assertEqual(self.s.execute.call_count, 2 + qtd_strains)
        self.s.execute.assert_called_with('update_strain_code',
                                          {'code': 'CB 030 MAI',
                                           'id_strain': 3})
        self.assertTrue(self.s.fetch.called)
        self.s.fetch.assert_called_with('all')

        self.assertTrue(self.s.dbconnection.connect.commit.called)

    def testInvalidUpdateDivisionPatternRaisesExcepetion(self):
        self.assertRaises(StrainFormatterError, self.s.update_division_pattern, 1, 'DEFAULT', 'CBMAI')
        self.assertFalse(self.s.execute.called)

    def testValidInsertDivisionOk(self):
        self.s.fetch.return_value = 1

        self.assertEqual(self.s.insert_division(1, 'CBMAI ####', 'DEFAULT'), 1)

        self.assertEqual(self.s.execute.call_count, 2)
        self.s.execute.assert_called_with('last_insert_id')
        self.assertTrue(self.s.fetch.called)
        self.s.fetch.assert_called_with('one')

        self.assertTrue(self.s.dbconnection.connect.commit.called)

    def testInvalidInsertDivisionRaisesException(self):
        self.assertRaises(StrainFormatterError, self.s.insert_division, 1, 'CBMAI', 'DEF')
        self.assertFalse(self.s.execute.called)

    def testDeleteDivisionNotInUseOk(self):
        self.s.fetch.return_value = ''

        id_division = 5
        self.assertTrue(self.s.delete_division(id_division))
        self.assertEqual(self.s.execute.call_count, 2)
        self.s.execute.assert_called_with('delete_division', {'id_division': id_division, })
        self.assertTrue(self.s.fetch.called)
        self.s.fetch.assert_called_with('one')

        self.assertTrue(self.s.dbconnection.connect.commit.called)

    def testDeleteDivisionInUseRaisesException(self):
        self.s.fetch.return_value = 3

        id_division = 1
        self.assertRaises(StrainFormatterError, self.s.delete_division, id_division)

        self.assertEqual(self.s.execute.call_count, 1)
        self.s.execute.assert_called_with('count_strains_using_division', {'id_division': id_division, })
        self.assertTrue(self.s.fetch.called)
        self.s.fetch.assert_called_with('one')

    def testDivisionSelectOptionsWithSelectedOptionOk(self):
        self.s.get_division_list = Mock()
        self.s.get_division_list.return_value = [
            {'id_division': 1, 'division':'DEFAULT'},
            {'id_division': 2, 'division':'ANT'}
        ]

        expected_options = '''<option selected value="1">DEFAULT</option>\n<option value="2">ANT</option>'''

        id_subcoll = 1
        id_division = 1

        self.assertEqual(self.s.division_select_options(id_subcoll, id_division), expected_options)
        self.assertTrue(self.s.get_division_list.called)
        self.s.get_division_list.assert_called_with(id_subcoll)

    def testDivisionSelectOptionsWithNoSelectedOptionOk(self):
        self.s.get_division_list = Mock()
        self.s.get_division_list.return_value = [
            {'id_division': 1, 'division':'DEFAULT'},
            {'id_division': 2, 'division':'ANT'}
        ]

        expected_options = '''<option value="1">DEFAULT</option>\n<option value="2">ANT</option>'''

        id_subcoll = 1

        self.assertEqual(self.s.division_select_options(id_subcoll), expected_options)
        self.assertTrue(self.s.get_division_list.called)
        self.s.get_division_list.assert_called_with(id_subcoll)

    def testDivisionJavascriptOptionsOk(self):
        self.s.get_division_list = Mock()
        self.s.get_division_list.return_value = [
            {'id_division': 1, 'division':'DEFAULT', 'pattern': 'CBMAI ####'},
            {'id_division': 2, 'division':'ANT', 'pattern': 'CBMAI A-###'},
        ]

        expected_options = "strain_format['1'] = 'CBMAI %04d';\nstrain_format['2'] = 'CBMAI A-%03d';"

        id_subcoll = 1

        self.assertEqual(self.s.division_javascript_options(id_subcoll), expected_options)
        self.assertTrue(self.s.get_division_list.called)
        self.s.get_division_list.assert_called_with(id_subcoll)

    def tearDown(self):
        super(StrainFormatterTestCase, self).tearDown()

        self.dbConnection_patcher.stop()

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from mock import Mock, patch, MagicMock
import unittest

from utilities import Utilities


class UtilitiesTestCase(unittest.TestCase):
    def setUp(self):
        super(UtilitiesTestCase, self).setUp()

        self.dbConnection_patcher = patch('utilities.dbConnection')
        self.General_patcher = patch('utilities.General')
        self.Getdata_patcher = patch('utilities.Getdata')
        self.Log_patcher = patch('utilities.Log')
        self.Logging_patcher = patch('utilities.Logging')
        self.Session_patcher = patch('utilities.Session')
        self.Utilities_patcher = patch.object(
            Utilities,
            'build_base_descr',
            MagicMock)

        self.dbConnection_patcher.start()
        self.General_patcher.start()
        self.Getdata_patcher.start()
        self.Log_patcher.start()
        self.Logging_patcher.start()
        session_patch = self.Session_patcher.start()
        session_patch.return_value = MagicMock()
        self.Utilities_patcher.start()

        self.u = Utilities('cOoKiE')

    def test_validate_date_mask(self):
        result = self.u.validate_date_mask(None)
        self.assertFalse(result)

        result = self.u.validate_date_mask('')
        self.assertFalse(result)

        result = self.u.validate_date_mask('%d/%m/%Y')
        self.assertEqual(result, '%d/%m/%Y')

    def test_get_date_time_format(self):
        get_date_format_mock = Mock()
        get_date_format_mock.return_value = '%d/%m/%Y'

        patcher = patch.object(self.u, 'get_date_format', get_date_format_mock)
        patcher.start()

        result = self.u.get_date_time_format()
        self.assertEqual(get_date_format_mock.call_count, 1)
        self.assertEqual(result, '%d/%m/%Y %H:%M:%S')

        patcher.stop()

    def test_format_date_time(self):
        result = self.u.format_date_time(None)
        self.assertEqual(result, '')

        result = self.u.format_date_time('')
        self.assertEqual(result, '')

        result = self.u.format_date_time(0)
        self.assertEqual(result, '')

        # Happy path
        get_date_time_format_mock = Mock()
        get_date_time_format_mock.return_value = '%d/%m/%Y %H:%M:%S'

        patcher = patch.object(
            self.u,
            'get_date_time_format',
            get_date_time_format_mock)

        patcher.start()

        field_mock = Mock()
        field_mock.timetuple.return_value = (1987, 1, 27, 20, 38, 0, 0, 0, 0)

        result = self.u.format_date_time(field_mock)
        self.assertEqual(get_date_time_format_mock.call_count, 1)
        self.assertEqual(field_mock.timetuple.call_count, 1)
        self.assertEqual(result, '27/01/1987 20:38:00')

        patcher.stop()

    def test_get_date_format_in_session(self):
        self.u.session.data = MagicMock()
        data_mock = self.u.session.data

        validate_date_mask_mock = Mock()
        validate_date_mask_mock.return_value = '%d-%m-%Y'

        patcher = patch.object(
            self.u,
            'validate_date_mask',
            validate_date_mask_mock)

        patcher.start()

        result = self.u.get_date_format()
        data_mock.__getitem__.assert_called_once_with('date_output_mask')
        self.assertEqual(validate_date_mask_mock.call_count, 1)
        self.assertEqual(result, '%d-%m-%Y')

        patcher.stop()

    def test_get_date_format_in_config(self):
        return_values = [False, '%m-%d-%Y']

        def side_effect(*args, **kwargs):
            return return_values.pop(0)

        validate_date_mask_mock = Mock()
        validate_date_mask_mock.side_effect = side_effect

        self.u.g = Mock()

        patcher = patch.object(
            self.u,
            'validate_date_mask',
            validate_date_mask_mock)

        patcher.start()

        result = self.u.get_date_format()
        self.u.g.get_config.assert_called_once_with('date_output_mask')
        self.assertEqual(validate_date_mask_mock.call_count, 2)
        self.assertEqual(result, '%m-%d-%Y')

        patcher.stop()

    def test_get_date_format_fallback(self):
        validate_date_mask_mock = Mock()
        validate_date_mask_mock.return_value = False

        patcher = patch.object(
            self.u,
            'validate_date_mask',
            validate_date_mask_mock)

        patcher.start()

        result = self.u.get_date_format()
        self.assertEqual(validate_date_mask_mock.call_count, 2)
        self.assertEqual(result, '%d/%m/%Y')

        patcher.stop()

    def tearDown(self):
        super(UtilitiesTestCase, self).tearDown()

        self.dbConnection_patcher.stop()
        self.General_patcher.stop()
        self.Getdata_patcher.stop()
        self.Log_patcher.stop()
        self.Logging_patcher.stop()
        self.Session_patcher.stop()
        self.Utilities_patcher.stop()

if __name__ == "__main__":
    unittest.main()

import os
import sys
import time
import unittest
import jc.utils

# Set the timezone on POSIX systems. Need to manually set for Windows tests
if not sys.platform.startswith('win32'):
    os.environ['TZ'] = 'America/Los_Angeles'
    time.tzset()


class MyTests(unittest.TestCase):

    def test_utils_timestamp(self):
        # naive timestamps created in PDT
        datetime_map = {
            # C locale format conversion, or date cli command in C locale with non-UTC tz
            'Tue Mar 23 16:12:11 2021': {'string': 'Tue Mar 23 16:12:11 2021', 'format': 1000, 'naive': 1616541131, 'utc': None},
            'Tue Mar 23 16:12:11 IST 2021': {'string': 'Tue Mar 23 16:12:11 IST 2021', 'format': 1000, 'naive': 1616541131, 'utc': None},
            # Git date output
            'Thu Mar 5 09:17:40 2020 -0800': {'string': 'Thu Mar 5 09:17:40 2020 -0800', 'format': 1100, 'naive': 1583428660, 'utc': None},
            # ISO Format with UTC (found in syslog 5424)
            '2003-10-11T22:14:15.003Z': {'string': '2003-10-11T22:14:15.003Z', 'format': 1300, 'naive': 1065935655, 'utc': 1065910455},
            # ISO Format without TZ (found in syslog 5424)
            '2003-10-11T22:14:15.003': {'string': '2003-10-11T22:14:15.003', 'format': 1310, 'naive': 1065935655, 'utc': None},
            # CEF Format with UTC
            'Nov 08 2022 12:30:00.111 UTC': {'string': 'Nov 08 2022 12:30:00.111 UTC', 'format': 1400, 'naive': 1667939400, 'utc': 1667910600},
            # CEF Format without TZ
            'Nov 08 2022 12:30:00.111': {'string': 'Nov 08 2022 12:30:00.111', 'format': 1410, 'naive': 1667939400, 'utc': None},
            # CEF Format with UTC without microseconds
            'Nov 08 2022 12:30:00 UTC': {'string': 'Nov 08 2022 12:30:00 UTC', 'format': 1420, 'naive': 1667939400, 'utc': 1667910600},
            # CEF Format without TZ or microseconds
            'Nov 08 2022 12:30:00': {'string': 'Nov 08 2022 12:30:00', 'format': 1430, 'naive': 1667939400, 'utc': None},
            # en_US.UTF-8 local format (found in who cli output)
            '2021-03-23 00:14': {'string': '2021-03-23 00:14', 'format': 1500, 'naive': 1616483640, 'utc': None},
            # Windows english format (found in dir cli output)
            '12/07/2019 02:09 AM': {'string': '12/07/2019 02:09 AM', 'format': 1600, 'naive': 1575713340, 'utc': None},
            # Windows english format wint non-UTC tz (found in systeminfo cli output)
            '3/22/2021, 1:15:51 PM (UTC-0600)': {'string': '3/22/2021, 1:15:51 PM (UTC-0600)', 'format': 1700, 'naive': 1616444151, 'utc': None},
            # Windows english format with UTC tz (found in systeminfo cli output)
            '3/22/2021, 1:15:51 PM (UTC)': {'string': '3/22/2021, 1:15:51 PM (UTC)', 'format': 1705, 'naive': 1616444151, 'utc': 1616418951},
            # Windows english format with UTC tz in long-form (found in systeminfo cli output)
            '3/22/2021, 1:15:51 PM (Coordinated Universal Time)': {'string': '3/22/2021, 1:15:51 PM (Coordinated Universal Time)', 'format': 1705, 'naive': 1616444151, 'utc': 1616418951},
            # Windows english format with UTC tz (found in systeminfo cli output)
            '3/22/2021, 1:15:51 PM (UTC+0000)': {'string': '3/22/2021, 1:15:51 PM (UTC+0000)', 'format': 1710, 'naive': 1616444151, 'utc': 1616418951},
            # en_US.UTF-8 local format (found in upower cli output)
            'Tue 23 Mar 2021 04:12:11 PM UTC': {'string': 'Tue 23 Mar 2021 04:12:11 PM UTC', 'format': 2000, 'naive': 1616541131, 'utc': 1616515931},
            # en_US.UTF-8 local format with non-UTC tz (found in upower cli output)
            'Tue 23 Mar 2021 04:12:11 PM IST': {'string': 'Tue 23 Mar 2021 04:12:11 PM IST', 'format': 3000, 'naive': 1616541131, 'utc': None},
            # European local format (found in upower cli output)
            'Tuesday 01 October 2019 12:50:41 PM UTC': {'string': 'Tuesday 01 October 2019 12:50:41 PM UTC', 'format': 4000, 'naive': 1569959441, 'utc': 1569934241},
            # European local format with non-UTC tz (found in upower cli output)
            'Tuesday 01 October 2019 12:50:41 PM IST': {'string': 'Tuesday 01 October 2019 12:50:41 PM IST', 'format': 5000, 'naive': 1569959441, 'utc': None},
            # date cli command in en_US.UTF-8 format
            'Wed Mar 24 06:16:19 PM UTC 2021': {'string': 'Wed Mar 24 06:16:19 PM UTC 2021', 'format': 6000, 'naive': 1616634979, 'utc': 1616609779},
            # date cli command in C locale format
            'Wed Mar 24 11:11:30 UTC 2021': {'string': 'Wed Mar 24 11:11:30 UTC 2021', 'format': 7000, 'naive': 1616609490, 'utc': 1616584290},
            # C locale format (found in stat cli output - OSX)
            'Mar 29 11:49:05 2021': {'string': 'Mar 29 11:49:05 2021', 'format': 7100, 'naive': 1617043745, 'utc': None},
            # C local format (found in stat cli output - linux) non-UTC tz
            '2019-08-13 18:13:43.555604315 -0400': {'string': '2019-08-13 18:13:43.555604315 -0400', 'format': 7200, 'naive': 1565745223, 'utc': None},
            # C local format (found in stat cli output - linux) UTC
            '2019-08-13 18:13:43.555604315 -0000': {'string': '2019-08-13 18:13:43.555604315 -0000', 'format': 7200, 'naive': 1565745223, 'utc': 1565720023},
            # C locale format with non-UTC tz (found in modified vmstat cli output)
            '2021-09-16 20:32:28 PDT': {'string': '2021-09-16 20:32:28 PDT', 'format': 7250, 'naive': 1631849548, 'utc': None},
            # C locale format (found in modified vmstat cli output)
            '2021-09-16 20:32:28 UTC': {'string': '2021-09-16 20:32:28 UTC', 'format': 7255, 'naive': 1631849548, 'utc': 1631824348},
            # C locale format (found in timedatectl cli output)
            'Wed 2020-03-11 00:53:21 UTC': {'string': 'Wed 2020-03-11 00:53:21 UTC', 'format': 7300, 'naive': 1583913201, 'utc': 1583888001},
            # test with None input
            None: {'string': None, 'format': None, 'naive': None, 'utc': None}
        }

        for input_string, expected_output in datetime_map.items():
            self.assertEqual(jc.utils.timestamp(input_string).__dict__, expected_output)

    def test_utils_convert_to_int(self):
        io_map = {
            None: None,
            True: 1,
            False: 0,
            '': None,
            '0': 0,
            '1': 1,
            '-1': -1,
            '0.0': 0,
            '0.1': 0,
            '0.6': 0,
            '-0.1': 0,
            '-0.6': 0,
            0: 0,
            1: 1,
            -1: -1,
            0.0: 0,
            0.1: 0,
            0.6: 0,
            -0.1: 0,
            -0.6: 0
        }

        for input_string, expected_output in io_map.items():
            self.assertEqual(jc.utils.convert_to_int(input_string), expected_output)

    def test_utils_convert_to_float(self):
        io_map = {
            None: None,
            True: 1.0,
            False: 0.0,
            '': None,
            '0': 0.0,
            '1': 1.0,
            '-1': -1.0,
            '0.0': 0.0,
            '0.1': 0.1,
            '0.6': 0.6,
            '-0.1': -0.1,
            '-0.6': -0.6,
            0: 0.0,
            1: 1.0,
            -1: -1.0,
            0.0: 0.0,
            0.1: 0.1,
            0.6: 0.6,
            -0.1: -0.1,
            -0.6: -0.6
        }

        for input_string, expected_output in io_map.items():
            self.assertEqual(jc.utils.convert_to_float(input_string), expected_output)

    def test_utils_convert_to_bool(self):
        io_map = {
            None: False,
            True: True,
            False: False,
            '': False,
            '0': False,
            '1': True,
            '-1': True,
            '0.0': False,
            '0.1': True,
            '-0.1': True,
            '*': True,
            'true': True,
            'True': True,
            'false': False,
            'False': False,
            'Y': True,
            'y': True,
            'Yes': True,
            'n': False,
            'N': False,
            'No': False,
            0: False,
            1: True,
            -1: True,
            0.0: False,
            0.1: True,
            -0.1: True,
        }

        for input_string, expected_output in io_map.items():
            self.assertEqual(jc.utils.convert_to_bool(input_string), expected_output)


    def test_has_data_nodata(self):
        self.assertFalse(jc.utils.has_data('     \n      '))


    def test_has_data_withdata(self):
        self.assertTrue(jc.utils.has_data('     \n  abcd    \n    '))


    def test_input_type_check_wrong(self):
        self.assertRaises(TypeError, jc.utils.input_type_check, ['abc'])


    def test_input_type_check_correct(self):
        self.assertEqual(jc.utils.input_type_check('abc'), None)


    # need to mock shutil.get_terminal_size().columns or add a column parameter to test
    # def test_warning_message(self):
    #     msg = [
    #         'this is a long first line that will be wrapped yada yada yada yada yada yada yada.',
    #         'this is a second long line that will be wrapped yada yada yada yada yada yada yada yada yada.',
    #         'this is a third long line that will be wrapped yada yada yada yada yada yada yada yada yada.'
    #     ]

    #     expected = '''jc:  Warning - this is a long first line that will be wrapped yada yada yada
    #            yada yada yada yada.
    #            this is a second long line that will be wrapped yada yada yada
    #                yada yada yada yada yada yada.
    #            this is a third long line that will be wrapped yada yada yada
    #                yada yada yada yada yada yada.'''

    #     f = io.StringIO()
    #     with contextlib.redirect_stderr(f):
    #         jc.utils.warning_message(msg)

    #     self.assertEqual(f.getvalue(), expected + '\n')



if __name__ == '__main__':
    unittest.main()

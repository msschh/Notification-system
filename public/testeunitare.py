import unittest

from mock import patch
from datetime import datetime

from helper import getFullName
from db import DataBase
 
class TestHelper(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_helper_1(self):
        self.assertEqual(getFullName("alex", "en"), "alex en")

    def test_helper_2(self):
        self.assertEqual(getFullName("name", "name"), "name name")

    def test_helper_3(self):
        self.assertEqual(getFullName(" ", " "), "   ")

    def test_helper_4(self):
        self.assertNotEqual(getFullName("fname", "lname"), "fnamelname")


class TestDb(unittest.TestCase):

    def test_db_1(self):
        with patch.object(DataBase, "__init__", lambda x, y, z, t: None):
            d = DataBase(None, None, None)
            self.assertEqual(d.read_unread_news("241", "name@yahoo.com", 1), [])

    def test_db_2(self):
        with patch.object(DataBase, "__init__", lambda x, y, z, t: None):
            d = DataBase(None, None, None)
            self.assertEqual(d.read_unread_news("121", "email@gmail.com", 1), [])

    def test_db_string_to_date1(self):
        with patch.object(DataBase, "__init__", lambda x, y, z, t: None):
            d = DataBase(None, None, None)
            dat = '2018-12-23'
            form = '%Y-%m-%d'
            self.assertEqual(d.string_to_date(dat), datetime.strptime(dat, form))

    def test_db_string_to_date2(self):
        with patch.object(DataBase, "__init__", lambda x, y, z, t: None):
            d = DataBase(None, None, None)
            try:
                d.string_to_date('')
            except ValueError:
                return True
            return False

    def test_db_string_to_date3(self):
        with patch.object(DataBase, "__init__", lambda x, y, z, t: None):
            d = DataBase(None, None, None)
            try:
                d.string_to_date('23/10/2028')
            except ValueError:
                return True
            return False

    def test_db_string_to_date4(self):
        with patch.object(DataBase, "__init__", lambda x, y, z, t: None):
            d = DataBase(None, None, None)
            dat = '10/15/1999'
            form = '%m/%d/%Y'
            self.assertEqual(d.string_to_date(dat), datetime.strptime(dat, form))

if __name__ == '__main__':
    unittest.main()
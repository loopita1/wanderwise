import unittest
from gen import valid_date

class TestDate(unittest.TestCase):

    def test_valid_date(self):
        self.assertFalse(valid_date("06/24/2026"))
    
    def test_invalid_format(self):
        self.assertTrue(valid_date("04-20-2026"))

    def test_invalid_date(self):
        self.assertTrue(valid_date("16/24/2026"))
    
    def test_string(self):
        self.assertTrue(valid_date("hi"))

if __name__ == "__main__":
    unittest.main()
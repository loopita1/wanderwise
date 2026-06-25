import unittest
from gen import validDate

class TestDate(unittest.TestCase):

    def testValidDate(self):
        self.assertFalse(valid_date("06/24/2026"))
    
    def testInvalidFormat(self):
        self.assertTrue(valid_date("04-20-2026"))

    def testInvalidDate(self):
        self.assertTrue(valid_date("16/24/2026"))
    
    def testString(self):
        self.assertTrue(valid_date("hi"))

if __name__ == "__main__":
    unittest.main()
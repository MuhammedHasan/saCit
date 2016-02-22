import unittest
import settings
from extract import extract_all


class Tests_Extract(unittest.TestCase):

    def tests_extract_all(self):
        file_location = settings.PARSCIT_BIN_LOCATION + '/../demodata/sample2.txt'
        self.assertIsNotNone(extract_all(file_location))


if __name__ == '__main__':
    unittest.main()

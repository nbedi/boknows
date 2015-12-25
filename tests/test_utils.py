import unittest

from boknows import utils

class TestUtils(unittest.TestCase):
    def test_csv_cleanup(self):
        self.maxDiff = None
        files = {}
        
        with open('examples/test.csv', 'r') as f:
            files = utils.csv_cleanup(f.read())
        
            with open('examples/expected.csv', 'r') as f:
                self.assertEqual(files, f.read())

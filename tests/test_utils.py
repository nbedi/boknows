import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
import sys

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

from boknows import utils

class TestUtils(unittest.TestCase):
    def test_csv_cleanup(self):
        self.maxDiff = None
        files = {}    
        
        with open('examples/test.csv', 'r') as f:
            files = utils.csv_cleanup(f.read())
            
            assert_frame_equal(pd.read_csv(StringIO(files[1])), pd.read_csv(open('examples/expected.csv')))

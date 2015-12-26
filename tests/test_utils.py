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
            frame1 = pd.read_csv(StringIO(files[1])).sort_index(axis=1)
            frame2 = pd.read_csv(open('examples/expected.csv')).sort_index(axis=1)
            
            assert_frame_equal(frame1, frame2)

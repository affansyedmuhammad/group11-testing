import unittest

import config
from data_loader import DataLoader
from analyzer_one import AnalyzerOne

class TestAnalyzerOne(unittest.TestCase):

    def test_analysis_new(self):
        config.set_parameter('user', 'new')
        AnalyzerOne().run()

    def test_analysis_experienced(self):
        config.set_parameter('user', 'experienced')
        AnalyzerOne().run()
        
from typing import List
import unittest

import config
from data_loader import DataLoader
from analyzer_one import AnalyzerOne
from model import Issue

class TestAnalyzerOne(unittest.TestCase):

    def create_mock_data(self):
        self.issues: List[Issue] = DataLoader().get_issues()
        self.issues_subset_1 = self.issues[0]
        self.issues_subset_2 = self.issues[0:4]

    def test_analyze_new_developers_single_issue(self):
        self.create_mock_data()
        AnalyzerOne().analyze_new_developers(self.issues_subset_1)

    def test_analyze_experienced_developers_single_issue(self):
        self.create_mock_data()
        AnalyzerOne().analyze_experienced_developers(self.issues_subset_1)

    def test_analyze_new_developers_multiple_issue(self):
        self.create_mock_data()
        AnalyzerOne().analyze_new_developers(self.issues_subset_2)

    def test_analyze_experienced_developers_multiple_issue(self):
        self.create_mock_data()
        AnalyzerOne().analyze_experienced_developers(self.issues_subset_2)

    def test_analyze_new_developers_empty(self):
        AnalyzerOne().analyze_new_developers([])

    def test_analyze_experienced_developers_empty(self):
        AnalyzerOne().analyze_experienced_developers([])

    def test_analysis_failure(self):
        AnalyzerOne().run()

    def test_analysis_new(self):
        config.set_parameter('user', 'new')
        AnalyzerOne().run()

    def test_analysis_experienced(self):
        config.set_parameter('user', 'experienced')
        AnalyzerOne().run()

    def test_analysis_incorrect_user_value(self):
        config.set_parameter('user', 'senior')
        AnalyzerOne().run()

    def test_analysis_label(self):
        config.set_parameter('label', 'experienced')
        AnalyzerOne().run()
import unittest
from data_loader import DataLoader
import config

class TestDataLoader(unittest.TestCase):

    def test_get_issues(self):
        issue_list = DataLoader().get_issues()
        self.assertIsNotNone(issue_list)
        self.assertEqual(661, len(issue_list))

    # def test_get_issues_failure(self):
    #     data_loader = DataLoader()
    #     data_loader.data_path =  ""
    #     issue_list = data_loader.get_issues()
    #     self.assertEqual([], issue_list)
    #     self.assertEqual(0, len(issue_list))

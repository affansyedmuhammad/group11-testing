import unittest
from data_loader import DataLoader

class TestDataLoader(unittest.TestCase):

    def test_get_issues(self):
        issue_list = DataLoader().get_issues()
        self.assertIsNotNone(issue_list)
        self.assertEqual(661, len(issue_list))
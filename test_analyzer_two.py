import unittest
from unittest.mock import MagicMock, patch
from analyzer_two import AnalyzerTwo
from model import Issue, Event

class TestAnalyzerTwo(unittest.TestCase):

    def setUp(self):
        self.analyzer = AnalyzerTwo(mention_threshold=3)
        event1 = MagicMock()
        event1.event_type = 'mentioned'
        event1.author = 'user1'
        event2 = MagicMock()
        event2.event_type = 'mentioned'
        event2.author = 'user2'
        event3 = MagicMock()
        event3.event_type = 'mentioned'
        event3.author = 'user1'
        issue1 = MagicMock()
        issue1.events = [event1, event2, event3]
        event4 = MagicMock()
        event4.event_type = 'mentioned'
        event4.author = 'user1'
        event5 = MagicMock()
        event5.event_type = 'mentioned'
        event5.author = 'user3'
        event6 = MagicMock()
        event6.event_type = 'opened'
        event6.author = 'user4'

        issue2 = MagicMock()
        issue2.events = [event4, event5, event6]

        self.mock_issues = [issue1, issue2]

    @patch('analyzer_two.DataLoader')
    def test_count_mentions(self, MockDataLoader):
        MockDataLoader().get_issues.return_value = self.mock_issues
        mention_counts = self.analyzer.count_mentions(self.mock_issues)
        expected_counts = {
            'user1': 3,
            'user2': 1,
            'user3': 1,
        }
        self.assertEqual(mention_counts, expected_counts)

if __name__ == '__main__':
    unittest.main()

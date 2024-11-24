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

    @patch('analyzer_two.DataLoader')
    def test_count_mentions_none(self, MockDataLoader):
        MockDataLoader().get_issues.return_value = {}
        mention_counts = self.analyzer.count_mentions({})
        expected_counts = {}
        self.assertEqual(mention_counts, expected_counts)
    
    @patch('matplotlib.pyplot.show')
    def test_visualize_mentions(self, mock_show):
        mock_counts = {
            'user1': 10,
            'user2': 8,
            'user3': 5,
        }
        self.analyzer.visualize_mentions(mock_counts)
        mock_show.assert_called_once()

    @patch('builtins.input', side_effect=['user1', 'user3', 'unknown_user', 'quit'])
    @patch('builtins.print')
    def test_check_user_experience(self, mock_print, mock_input):
        mention_counts = {
            'user1': 4,
            'user2': 2,
            'user3': 1,
        }
        self.analyzer.check_user_experience(mention_counts)

        # Verify the expected output was printed
        mock_print.assert_any_call("user1 is an experienced contributor with 4 mentions.")
        mock_print.assert_any_call("user3 has been mentioned 1 times, which is below the experience threshold.")
        mock_print.assert_any_call("unknown_user has not been mentioned in any issues.")

    @patch('analyzer_two.DataLoader')
    @patch.object(AnalyzerTwo, 'count_mentions', return_value={'user1': 3, 'user2': 2})
    @patch.object(AnalyzerTwo, 'visualize_mentions')
    @patch.object(AnalyzerTwo, 'check_user_experience')
    def test_run(self, mock_check_user_experience, mock_visualize_mentions, mock_count_mentions, mock_data_loader):
        mock_issues = [MagicMock(), MagicMock()]
        mock_data_loader().get_issues.return_value = mock_issues

        analyzer = AnalyzerTwo(mention_threshold=3)
        analyzer.run()

        mock_data_loader().get_issues.assert_called_once()
        mock_count_mentions.assert_called_once_with(mock_issues)
        mock_visualize_mentions.assert_called_once_with({'user1': 3, 'user2': 2})
        mock_check_user_experience.assert_called_once_with({'user1': 3, 'user2': 2})

if __name__ == '__main__':
    unittest.main()

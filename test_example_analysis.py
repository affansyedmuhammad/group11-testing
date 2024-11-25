import unittest
from unittest.mock import patch
from example_analysis import ExampleAnalysis
from model import Issue, Event

class TestExampleAnalysis(unittest.TestCase):

    def setUp(self):
        # Create mock events
        self.event1 = Event({
            'event_type': 'commented',
            'author': 'user1',
        })
        self.event2 = Event({
            'event_type': 'labeled',
            'author': 'user2',
        })
        self.event3 = Event({
            'event_type': 'closed',
            'author': 'user1',
        })
        self.event4 = Event({
            'event_type': 'opened',
            'author': 'user3',
        })
        self.event5 = Event({
            'event_type': 'commented',
            'author': 'user2',
        })

        # Create mock issues
        self.issue1 = Issue({
            'creator': 'creator1',
            'state': 'open',
            'events': [
                {
                    'event_type': self.event1.event_type,
                    'author': self.event1.author,
                },
                {
                    'event_type': self.event2.event_type,
                    'author': self.event2.author,
                }
            ]
        })
        self.issue2 = Issue({
            'creator': 'creator2',
            'state': 'closed',
            'events': [
                {
                    'event_type': self.event3.event_type,
                    'author': self.event3.author,
                },
                {
                    'event_type': self.event4.event_type,
                    'author': self.event4.author,
                },
                {
                    'event_type': self.event5.event_type,
                    'author': self.event5.author,
                }
            ]
        })

        # Store the mock issues in a list
        self.mock_issues = [self.issue1, self.issue2]

    @patch('example_analysis.print')
    @patch('example_analysis.DataLoader')
    @patch('example_analysis.config.get_parameter')
    def test_run_total_events(self, mock_get_parameter, mock_data_loader, mock_print):
        mock_get_parameter.return_value = None  # No user filter

        # Mock DataLoader().get_issues() to return the mock issues
        mock_data_loader.return_value.get_issues.return_value = self.mock_issues

        analyzer = ExampleAnalysis()
        analyzer.run()
        expected_output = 'Found 5 events across 2 issues.'
        mock_print.assert_any_call('\n\n' + expected_output + '\n\n')

    @patch('example_analysis.print')
    @patch('example_analysis.DataLoader')
    @patch('example_analysis.config.get_parameter')
    def test_run_total_events_with_user(self, mock_get_parameter, mock_data_loader, mock_print):
        mock_get_parameter.return_value = 'user1'  # Filter by 'user1'

        # Mock DataLoader().get_issues()
        mock_data_loader.return_value.get_issues.return_value = self.mock_issues

        analyzer = ExampleAnalysis()
        analyzer.run()
        expected_output = 'Found 2 events across 2 issues for user1.'
        mock_print.assert_any_call('\n\n' + expected_output + '\n\n')

    @patch('example_analysis.plt.show')
    @patch('example_analysis.DataLoader')
    @patch('example_analysis.config.get_parameter')
    def test_run_plotting(self, mock_get_parameter, mock_data_loader, mock_plt_show):

        mock_get_parameter.return_value = None  # No user filter

        # Mock DataLoader().get_issues() to return the mock issues
        mock_data_loader.return_value.get_issues.return_value = self.mock_issues

        analyzer = ExampleAnalysis()
        analyzer.run()
        self.assertTrue(mock_plt_show.called)
        

if __name__ == '__main__':
    unittest.main()
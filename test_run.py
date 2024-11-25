import unittest
from unittest.mock import patch
import argparse
import run

class TestRunArgumentParsing(unittest.TestCase):
    @patch('sys.argv', ['run.py', '--feature', '1', '--user', 'testuser'])
    def test_parse_args_feature_one(self):
        args = run.parse_args()
        self.assertEqual(args.feature, 1)
        self.assertEqual(args.user, 'testuser')

    @patch('sys.argv', ['run.py', '--feature', '2', '--mention_threshold', '5'])
    def test_parse_args_feature_two(self):
        args = run.parse_args()
        self.assertEqual(args.feature, 2)
        self.assertEqual(args.mention_threshold, 5)

    @patch('sys.argv', ['run.py', '--feature', '3'])
    def test_parse_args_feature_three(self):
        args = run.parse_args()
        self.assertEqual(args.feature, 3)

    @patch('sys.argv', ['run.py', '--feature', '0'])
    def test_parse_args_example_analysis(self):
        args = run.parse_args()
        self.assertEqual(args.feature, 0)

    @patch('sys.argv', ['run.py', '--user', 'testuser'])
    def test_parse_args_missing_feature(self):
        with self.assertRaises(SystemExit):
            run.parse_args()

    @patch('sys.argv', ['run.py', '--feature', '1'])
    def test_parse_args_feature_one_missing_user(self):
        args = run.parse_args()
        self.assertEqual(args.feature, 1)
        self.assertIsNone(args.user)

    @patch('sys.argv', ['run.py', '--feature', '2'])
    def test_parse_args_feature_two_missing_threshold(self):
        args = run.parse_args()
        self.assertEqual(args.feature, 2)
        self.assertIsNone(args.mention_threshold)

    @patch('sys.argv', ['run.py', '--feature', '99'])
    def test_parse_args_invalid_feature(self):
        args = run.parse_args()
        self.assertEqual(args.feature, 99)


class TestRunFeatureExecution(unittest.TestCase):
    @patch('run.ExampleAnalysis')
    def test_run_example_analysis(self, mock_example_analysis):
        args = argparse.Namespace(feature=0)
        run.run_feature(args)
        mock_example_analysis.return_value.run.assert_called_once()

    @patch('run.print')
    @patch('run.AnalyzerOne')
    def test_run_feature_one_with_user(self, mock_analyzer_one, mock_print):
        args = argparse.Namespace(feature=1, user='testuser')
        run.run_feature(args)
        mock_print.assert_any_call('Running analysis for user: testuser')
        mock_analyzer_one.return_value.run.assert_called_once()

    @patch('run.print')
    def test_run_feature_one_missing_user(self, mock_print):
        args = argparse.Namespace(feature=1, user=None)
        run.run_feature(args)
        mock_print.assert_any_call('Error: Please specify a user with --user for feature 1.')

    @patch('run.print')
    @patch('run.AnalyzerTwo')
    def test_run_feature_two_with_threshold(self, mock_analyzer_two, mock_print):
        args = argparse.Namespace(feature=2, mention_threshold=5)
        run.run_feature(args)
        mock_print.assert_any_call('Running analysis with mention threshold: 5')
        mock_analyzer_two.assert_called_once_with(mention_threshold=5)
        mock_analyzer_two.return_value.run.assert_called_once()

    @patch('run.print')
    def test_run_feature_two_missing_threshold(self, mock_print):
        args = argparse.Namespace(feature=2, mention_threshold=None)
        run.run_feature(args)
        mock_print.assert_any_call('Error: Please specify a threshold with --mention_threshold for feature 2.')

    @patch('run.AnalyzerThree')
    def test_run_feature_three(self, mock_analyzer_three):
        args = argparse.Namespace(feature=3)
        run.run_feature(args)
        mock_analyzer_three.return_value.run.assert_called_once()

    @patch('run.print')
    def test_run_feature_invalid_feature(self, mock_print):
        args = argparse.Namespace(feature=99)
        run.run_feature(args)
        mock_print.assert_any_call('Unsupported feature number. Please specify a valid feature.')


if __name__ == '__main__':
    unittest.main()

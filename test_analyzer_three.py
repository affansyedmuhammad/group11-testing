import unittest
from unittest.mock import patch
from anaylzer_three import AnalyzerThree
from model import Issue


class TestAnalyzerThree(unittest.TestCase):

    def setUp(self):
        """Sets up reusable test data."""
        self.mock_issues = [
            Issue({
                "creator": "user1",
                "labels": ["bug", "enhancement"],
                "state": "open",
                "events": [
                    {"event_type": "commented", "author": "user2", "event_date": "2024-11-24T12:00:00"},
                    {"event_type": "commented", "author": "user3", "event_date": "2024-11-24T13:00:00"}
                ]
            }),
            Issue({
                "creator": "user2",
                "labels": ["bug"],
                "state": "closed",
                "events": [
                    {"event_type": "commented", "author": "user1", "event_date": "2024-11-24T14:00:00"},
                    {"event_type": "commented", "author": "user3", "event_date": "2024-11-24T15:00:00"},
                    {"event_type": "closed", "author": "user2", "event_date": "2024-11-24T16:00:00"}
                ]
            })
        ]
        self.empty_issues = []

    @patch("matplotlib.pyplot.show")
    def test_top_contributors_leaderboard(self, mock_show):
        """Checks if contributions are calculated correctly."""
        analyzer = AnalyzerThree()
        analyzer.TopContributorsLeaderboard(self.mock_issues)

        # Manually calculate expected contributions
        expected_counts = {"user1": 2, "user2": 3, "user3": 2}
        contributor_counts = {}
        for issue in self.mock_issues:
            contributor_counts[issue.creator] = contributor_counts.get(issue.creator, 0) + 1
            for event in issue.events:
                contributor_counts[event.author] = contributor_counts.get(event.author, 0) + 1

        # Assert actual contributions match expectations
        self.assertEqual(contributor_counts, expected_counts)

    @patch("matplotlib.pyplot.show")
    def test_engagement_levels_label(self, mock_show):
        """Checks engagement calculations for labels."""
        analyzer = AnalyzerThree()
        analyzer.EngagementLevelsLabel(self.mock_issues)

        # Manually compute expected engagement
        expected_label_engagement = {"bug": 5, "enhancement": 2}
        label_engagement = {}
        for issue in self.mock_issues:
            for label in issue.labels:
                label_engagement[label] = label_engagement.get(label, 0) + len(issue.events)

        # Assert engagement calculations match expectations
        self.assertEqual(label_engagement, expected_label_engagement)

    @patch.object(AnalyzerThree, "TopContributorsLeaderboard")
    @patch.object(AnalyzerThree, "EngagementLevelsLabel")
    def test_generate_plots(self, mock_engagement, mock_top):
        """Verifies that generate_plots calls the correct methods."""
        analyzer = AnalyzerThree()
        analyzer.generate_plots(self.mock_issues)

        # Ensure plotting methods were called once
        mock_top.assert_called_once_with(self.mock_issues)
        mock_engagement.assert_called_once_with(self.mock_issues)

    @patch("data_loader.DataLoader.get_issues", return_value=[])
    @patch.object(AnalyzerThree, "generate_plots")
    def test_run(self, mock_generate_plots, mock_get_issues):
        """Checks the overall run method."""
        analyzer = AnalyzerThree()
        analyzer.run()

        # Confirm data was loaded and plots were generated
        mock_get_issues.assert_called_once()
        mock_generate_plots.assert_called_once_with([])

    @patch("matplotlib.pyplot.show")
    def test_empty_input(self, mock_show):
        """Ensures methods handle empty input gracefully."""
        analyzer = AnalyzerThree()

        with self.assertRaises(ValueError):
            analyzer.TopContributorsLeaderboard(self.empty_issues)

        with self.assertRaises(ValueError):
            analyzer.EngagementLevelsLabel(self.empty_issues)

    @patch("matplotlib.pyplot.show")
    def test_partial_data(self, mock_show):
        """Tests handling of partial data."""
        partial_issues = [
            Issue({
                "creator": "user1",
                "labels": [],
                "state": "open",
                "events": []
            }),
            Issue({
                "creator": "user2",
                "labels": ["bug"],
                "state": "closed",
                "events": [
                    {"event_type": "closed", "author": "user2", "event_date": "2024-11-24T16:00:00"}
                ]
            })
        ]
        analyzer = AnalyzerThree()
        analyzer.TopContributorsLeaderboard(partial_issues)
        analyzer.EngagementLevelsLabel(partial_issues)

    def test_invalid_input(self):
        """Checks if invalid input throws the expected errors."""
        analyzer = AnalyzerThree()

        with self.assertRaises(AttributeError):
            analyzer.TopContributorsLeaderboard("invalid input")

        with self.assertRaises(AttributeError):
            analyzer.EngagementLevelsLabel("invalid input")


if __name__ == "__main__":
    unittest.main()

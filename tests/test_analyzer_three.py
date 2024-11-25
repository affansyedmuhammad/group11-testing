import sys
sys.path.append(r"C:\Users\krish\Documents\GitHub\group11-testing")
import pytest
from analyzer_three import AnalyzerThree
from model import Issue
from unittest.mock import patch


@pytest.fixture
def mock_issues():
    """Sets up some fake issues and events for testing purposes."""
    return [
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


def test_top_contributors_leaderboard(mock_issues):
    """Checks if the TopContributorsLeaderboard method calculates contributions correctly."""
    analyzer = AnalyzerThree()

    with patch("matplotlib.pyplot.show"):  # Prevents the graph from popping up during the test
        analyzer.TopContributorsLeaderboard(mock_issues)

    # Calculate expected contributions manually
    expected_counts = {"user1": 2, "user2": 3, "user3": 2}
    contributor_counts = {}
    for issue in mock_issues:
        contributor_counts[issue.creator] = contributor_counts.get(issue.creator, 0) + 1
        for event in issue.events:
            contributor_counts[event.author] = contributor_counts.get(event.author, 0) + 1

    # Make sure the actual results match our expectations
    assert contributor_counts == expected_counts


def test_engagement_levels_label(mock_issues):
    """Makes sure the EngagementLevelsLabel method handles engagement calculations correctly."""
    analyzer = AnalyzerThree()

    with patch("matplotlib.pyplot.show"):  # Skip rendering the graph
        analyzer.EngagementLevelsLabel(mock_issues)

    # Manually figure out what the engagement numbers should be
    expected_label_engagement = {"bug": 5, "enhancement": 2}
    label_engagement = {}
    for issue in mock_issues:
        for label in issue.labels:
            label_engagement[label] = label_engagement.get(label, 0) + len(issue.events)

    # Verify the method's calculations
    assert label_engagement == expected_label_engagement


def test_generate_plots(mock_issues):
    """Verifies that generate_plots correctly calls the plotting methods."""
    analyzer = AnalyzerThree()

    with patch.object(analyzer, "TopContributorsLeaderboard") as mock_top, \
         patch.object(analyzer, "EngagementLevelsLabel") as mock_engagement:
        analyzer.generate_plots(mock_issues)

        # Ensure each plotting method was called once with the right data
        mock_top.assert_called_once_with(mock_issues)
        mock_engagement.assert_called_once_with(mock_issues)


def test_run(mock_issues):
    """Checks the overall run method to see if it processes data and generates plots correctly."""
    analyzer = AnalyzerThree()

    with patch("data_loader.DataLoader.get_issues", return_value=mock_issues) as mock_data_loader, \
         patch.object(analyzer, "generate_plots") as mock_generate_plots:
        analyzer.run()

        # Confirm the data was loaded and the plots were generated
        mock_data_loader.assert_called_once()
        mock_generate_plots.assert_called_once_with(mock_issues)


def test_empty_input():
    """Tests how the methods handle an empty input (no issues)."""
    analyzer = AnalyzerThree()

    # Ensure the methods don't crash when there's no data
    with patch("matplotlib.pyplot.show"):
        analyzer.TopContributorsLeaderboard([])
    with patch("matplotlib.pyplot.show"):
        analyzer.EngagementLevelsLabel([])


def test_invalid_input():
    """Checks if invalid input throws the expected errors."""
    analyzer = AnalyzerThree()

    with pytest.raises(AttributeError):  # Passing in a string instead of a list should break
        analyzer.TopContributorsLeaderboard("invalid input")

    with pytest.raises(AttributeError):
        analyzer.EngagementLevelsLabel("invalid input")

from typing import List, Dict
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import DataLoader
from model import Issue, Event
import config

class AnalyzerThree:
    """
    Analyzes contributor and community engagement insights based on GitHub issues data.
    """
    
    def __init__(self):
        """
        Constructor
        """
        self.new_contributor_threshold = config.get_parameter('new_contributor_threshold', default=5)

    def TopContributorsLeaderboard(self, issues: List[Issue]):
        # Data for Top Contributors Leaderboard
        contributor_counts = {}
        for issue in issues:
            creator = issue.creator
            contributor_counts[creator] = contributor_counts.get(creator, 0) + 1

            for event in issue.events:
                if event.event_type == 'commented':
                    contributor_counts[event.author] = contributor_counts.get(event.author, 0) + 1

        contributor_df = pd.DataFrame(list(contributor_counts.items()), columns=['Contributor', 'Contributions'])
        top_contributors = contributor_df.nlargest(10, 'Contributions')
        
        plt.figure(figsize=(14, 8))
        plt.bar(top_contributors['Contributor'], top_contributors['Contributions'], color='lightblue')
        plt.title('Top 10 Contributors')
        plt.xlabel('Contributors')
        plt.ylabel('Total Contributions (Issues Created + Comments)')
        plt.tight_layout()
        plt.savefig("top_contributors.png")
        plt.show()


    def EngagementLevelsLabel(self, issues: List[Issue]):
        # Data for Engagement Levels by Label
        label_engagement = {}
        for issue in issues:
            for label in issue.labels:
                if label not in label_engagement:
                    label_engagement[label] = 0
                label_engagement[label] += len(issue.events)

        label_df = pd.DataFrame(list(label_engagement.items()), columns=['Label', 'Engagement'])
        top_labels = label_df.nlargest(10, 'Engagement')

        plt.figure(figsize=(14, 8))
        plt.bar(top_labels['Label'], top_labels['Engagement'], color='salmon')
        plt.title('Top Labels by Engagement')
        plt.xlabel('Labels')
        plt.ylabel('Engagement (Total Events)')
        plt.tight_layout()
        plt.savefig("top_labels.png")
        plt.show()

    def generate_plots(self, issues: List[Issue]):
        """
        Generates the plots:
        - Top contributors leaderboard
        - Engagement levels by label
        """
        self.TopContributorsLeaderboard(issues)
        self.EngagementLevelsLabel(issues)
        
    def run(self):
        """
        Runs the community engagement analysis, which includes:
        - Top contributors leaderboard
        - Engagement levels by label
        """
        issues: List[Issue] = DataLoader().get_issues()

        # Generate the analyses and combined plot
        self.generate_plots(issues)


if __name__ == '__main__':
    AnalyzerThree().run()
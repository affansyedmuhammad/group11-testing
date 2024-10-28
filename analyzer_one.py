from typing import List
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import DataLoader
from model import Issue
import config

class AnalyzerOne:
    """
    Implements analysis for new and experienced developers based on GitHub issues.
    """
    
    def __init__(self):
        """
        Constructor
        """
        # Parameter is passed in via command line (--user)
        self.EXPERIENCE_LEVEL: str = config.get_parameter('user')
    
    def run(self):
        """
        Runs the analysis based on the experience level.
        """
        issues: List[Issue] = DataLoader().get_issues()
        
        # Calculate time-to-close and collaboration levels
        for issue in issues:
            issue.time_to_close = (issue.updated_date - issue.created_date).total_seconds() / 3600
            issue.collaboration_level = len(issue.events)

        if self.EXPERIENCE_LEVEL == 'new':
            self.analyze_new_developers(issues)

        elif self.EXPERIENCE_LEVEL == 'experienced':
            self.analyze_experienced_developers(issues)

    def analyze_new_developers(self, issues: List[Issue]):
        """
        Analyzes issues suitable for new developers and plots a graph of labels vs. average time to close.
        """
        # Filter quick-to-resolve issues
        quick_issues = [issue for issue in issues if issue.time_to_close < pd.Series([i.time_to_close for i in issues]).median()]
        
        # Calculate average time to close per label
        label_times = {}
        for issue in quick_issues:
            for label in issue.labels:
                if label not in label_times:
                    label_times[label] = []
                label_times[label].append(issue.time_to_close)
        
        avg_label_times = {label: sum(times) / len(times) for label, times in label_times.items()}
        
        # Plotting
        labels, avg_times = zip(*sorted(avg_label_times.items(), key=lambda x: x[1]))
        
        plt.figure(figsize=(14, 8))
        plt.bar(labels, avg_times)
        plt.xlabel('Labels')
        plt.ylabel('Average Time to Close (hours)')
        plt.title('Average Time to Close by Label for New Developers')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def analyze_experienced_developers(self, issues: List[Issue]):
        pass
if __name__ == '__main__':
    AnalyzerOne().run()

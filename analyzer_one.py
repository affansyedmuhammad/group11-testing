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

    def analyze_experienced_developers(self, issues: List[Issue]):
        """
        Analyzes issues suitable for experienced developers by creating a bar chart of most active labels
        and a color-coded scatter plot of issue complexity.
        """
        # Calculate total events/comments for each label
        label_event_counts = {}
        for issue in issues:
            for label in issue.labels:
                if label not in label_event_counts:
                    label_event_counts[label] = 0
                label_event_counts[label] += len(issue.events)
        
        # Convert to DataFrame and get top 10 labels
        label_df = pd.DataFrame(list(label_event_counts.items()), columns=['Label', 'Total Events'])
        top_labels = label_df.nlargest(10, 'Total Events')
        
        # Plotting the first graph
        plt.figure(figsize=(10, 6))
        plt.bar(top_labels['Label'], top_labels['Total Events'], color='lightblue')
        plt.xlabel('Labels')
        plt.ylabel('Total Events/Comments')
        plt.title('Top 10 Most Active Labels')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()  # Display the first graph and wait until it's closed
        
        # Prepare data for scatter plot
        open_issues = [issue for issue in issues if issue.state == 'open']
        x = [len(issue.events) for issue in open_issues]
        y = [(issue.updated_date - issue.created_date).total_seconds() / 3600 for issue in open_issues]
        
        # Plotting the second graph
        plt.figure(figsize=(10, 6))
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        top_5_labels = top_labels['Label'].head().tolist()
        
        for i, label in enumerate(top_5_labels):
            label_issues = [issue for issue in open_issues if label in issue.labels]
            label_x = [len(issue.events) for issue in label_issues]
            label_y = [(issue.updated_date - issue.created_date).total_seconds() / 3600 for issue in label_issues]
            plt.scatter(label_x, label_y, c=colors[i], alpha=0.7, label=f"{label} ({label_event_counts[label]} events)")
        
        # Add other issues in grey
        other_issues = [issue for issue in open_issues if not any(label in issue.labels for label in top_5_labels)]
        other_x = [len(issue.events) for issue in other_issues]
        other_y = [(issue.updated_date - issue.created_date).total_seconds() / 3600 for issue in other_issues]
        plt.scatter(other_x, other_y, c='grey', alpha=0.3, label='Other')
        
        plt.xlabel('Total Events/Comments')
        plt.ylabel('Time Open (hours)')
        plt.title('Issue Complexity for Open Issues (Top 5 Labels Highlighted)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()  # Display the second graph after the first one is closed
        
        print("Top 10 most active labels:")
        print(top_labels.to_string(index=False))


if __name__ == '__main__':
    AnalyzerOne().run()

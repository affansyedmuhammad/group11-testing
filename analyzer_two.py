from typing import List, Dict
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import DataLoader
from model import Issue
import config

class AnalyzerTwo:
    """
    Analyzes GitHub issues to identify experienced contributors based on how often they are mentioned in comments.
    """
    
    def __init__(self, mention_threshold: int = 3):
        """
        Constructor
        """
        self.EXPERIENCE_THRESHOLD: int = mention_threshold
    
    def run(self):
        """
        Runs the analysis on user mentions in issues.
        """
        issues: List[Issue] = DataLoader().get_issues()
        mention_counts = self.count_mentions(issues)
        self.visualize_mentions(mention_counts)
        self.check_user_experience(mention_counts)

    def count_mentions(self, issues: List[Issue]) -> Dict[str, int]:
        """
        Counts how many times each user is mentioned across all issues.
        """
        mention_counts = {}
        for issue in issues:
            for event in issue.events:
                # Access attributes directly if event is not a dictionary
                if event.event_type == 'mentioned':
                    mentioned_user = event.author
                    mention_counts[mentioned_user] = mention_counts.get(mentioned_user, 0) + 1
        return mention_counts

    def visualize_mentions(self, mention_counts: Dict[str, int]):
        """
        Creates a bar chart of the top mentioned users.
        """
        mention_df = pd.DataFrame(list(mention_counts.items()), columns=['User', 'Mentions'])
        top_mentions = mention_df.nlargest(10, 'Mentions')
        
        plt.figure(figsize=(12, 6))
        plt.bar(top_mentions['User'], top_mentions['Mentions'], color='lightgreen')
        plt.xlabel('Users')
        plt.ylabel('Number of Mentions')
        plt.title('Top 10 Most Mentioned Users in Comments')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def check_user_experience(self, mention_counts: Dict[str, int]):
        """
        Allows checking the experience level of a specific user based on their mention count.
        """
        while True:
            username = input("Enter a username to check their experience (or 'quit' to exit): ")
            if username.lower() == 'quit':
                break
            if username in mention_counts:
                mentions = mention_counts[username]
                if mentions >= self.EXPERIENCE_THRESHOLD:
                    print(f"{username} is an experienced contributor with {mentions} mentions.")
                else:
                    print(f"{username} has been mentioned {mentions} times, which is below the experience threshold.")
            else:
                print(f"{username} has not been mentioned in any issues.")

if __name__ == '__main__':
    AnalyzerTwo().run()

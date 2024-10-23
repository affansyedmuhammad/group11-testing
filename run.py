import argparse
from analyzer_one import AnalyzerOne
from analyzer_two import AnalyzerTwo
from anaylzer_three import AnalyzerThree
import config
from example_analysis import ExampleAnalysis


def parse_args():
    """
    Parses the command line arguments that were provided along
    with the python command. The --feature flag must be provided as
    that determines what analysis to run. Optionally, you can pass in
    a user and/or a label to run analysis focusing on specific issues.
    
    You can also add more command line arguments following the pattern
    below.
    """
    ap = argparse.ArgumentParser("run.py")
    
    # Required parameter specifying what analysis to run
    ap.add_argument('--feature', '-f', type=int, required=True,
                    help='Which of the features to run')
    
    # Optional parameter for analyses focusing on a specific user (i.e., contributor)
    ap.add_argument('--user', '-u', type=str, required=False,
                    help='Optional parameter for analyses focusing on a specific user')
    
    # Optional parameter for analyses focusing on a specific label
    ap.add_argument('--label', '-l', type=str, required=False,
                    help='Optional parameter for analyses focusing on a specific label')
    
    return ap.parse_args()


def run_example_analysis():
    ExampleAnalysis().run()

def run_analyzer_one(args):
    if args.user:
        print(f'Running analysis for user: {args.user}')
        AnalyzerOne().run()
    else:
        print('Error: Please specify a user with --user for feature 1.')

def run_feature_two():
    AnalyzerTwo().run()

def run_feature_three():
    AnalyzerThree().run()


def run_feature(args):
    """Execute feature based on parsed arguments."""
    feature_map = {
        0: run_example_analysis,
        1: lambda: run_analyzer_one(args),
        2: run_feature_two,
        3: run_feature_three
    }

    feature_function = feature_map.get(args.feature)

    if feature_function:
        feature_function()
    else:
        print('Unsupported feature number. Please specify a valid feature.')


if __name__ == '__main__':
    try:
        args = parse_args()
        config.overwrite_from_args(args)
        run_feature(args)
    except SystemExit:
        pass
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

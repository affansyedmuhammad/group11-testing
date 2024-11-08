# ENPM611 GitHub Issues Analyzer

This repository contains an application developed for the ENPM611 class project. The application analyzes GitHub issues from the [Poetry](https://github.com/python-poetry/poetry/issues) open-source project to generate insightful analyses that assist developers.

## Overview

The application focuses on analyzing GitHub issues to help both new and experienced developers contribute effectively to the project. It provides tailored insights based on the developer's experience level:

-   **Feature 1**: Performs Developer-Specific Issue Analysis on poetry_issues.json
-   **Feature 2**: (To be added)
-   **Feature 3**: (To be added)

## Features

The application implements three main features (analyses), with the first feature currently developed:

### Feature 1: Developer-Specific Issue Analysis

#### Sub-analysis for New Developers

-   **Description**: Analyzes issues that have a shorter time-to-close, indicating they are easier to resolve.
-   **Output**: Generates a bar chart showing the average time to close issues per label, helping new developers identify suitable issues to work on.

#### Sub-analysis for Experienced Developers

-   **Description**: Analyzes issues with high collaboration levels (more comments and events), which are typically more complex and require experienced input.
-   **Output**:
    -   **Bar Chart**: Displays the top 10 most active labels based on the total number of events/comments.
    -   **Scatter Plot**: Visualizes open issues' complexity, highlighting issues with high collaboration and long open times.

### Feature 2: (Placeholder)

-   **Description**: To be developed.

### Feature 3: (Placeholder)

-   **Description**: To be developed.

## Setup

### Prerequisites

-   Python 3.7 or higher
-   pip (Python package installer)

### Install Dependencies

1. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment**:

    - On **Windows**:

        ```bash
        venv\Scripts\activate
        ```

    - On **Unix or macOS**:

        ```bash
        source venv/bin/activate
        ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

### Configure the Data File

1. **Download the data file** (`poetry_issues.json`) from the project assignment on Canvas.
2. **Update the `config.json` file** with the path to the data file:

    ```json
    {
        "data_path": "path/to/poetry_issues.json"
    }
    ```

    Alternatively, you can set an environment variable `ENPM611_PROJECT_DATA_PATH` with the path to the data file to avoid committing personal paths to the repository.

## How to Run the Application

The application is executed via the `run.py` script, using the `--feature` command-line argument to specify which analysis to run. For Feature 1, you can further specify the developer experience level using the `--user` argument.

### Running Feature 1

#### For New Developers

To run the analysis tailored for new developers:

```bash
python run.py --feature 1 --user new
```

-   **What It Does**: Analyzes issues with a shorter time-to-close and generates a bar chart of labels versus average time to close.
-   **How It Helps**: Helps new developers find issues that are quicker to resolve, easing their onboarding process into the project.

#### For Experienced Developers

To run the analysis tailored for experienced developers:

```bash
python run.py --feature 1 --user experienced
```

-   **What It Does**: Analyzes issues with high collaboration levels and generates:
    -   A bar chart of the top 10 most active labels.
    -   A scatter plot highlighting complex open issues.
-   **How It Helps**: Assists experienced developers in identifying complex issues where their expertise can make a significant impact.

### Running Feature 0 (Example Analysis)

An example analysis is provided to demonstrate basic functionality:

```bash
python run.py --feature 0
```

### Running Future Features

As Features 2 and 3 are developed, they can be executed similarly by specifying the appropriate feature number:

```bash
python run.py --feature 2
python run.py --feature 3
```

## VSCode Run Configuration

For easier debugging and execution, runtime configurations are provided for VSCode:

1. Open the **Run and Debug** view in VSCode.
2. Choose the desired analysis from the available configurations.
3. Start the debugger to run the selected analysis.

The configurations are specified in the `.vscode/launch.json` file.

## Additional Notes

-   **Environment Variables**: Use environment variables to set configuration parameters without modifying the `config.json` file.
-   **Extensibility**: The application is designed to be extensible. New analyses can be added by implementing additional features and updating the `run.py` script accordingly.
-   **Data Model and Utilities**:
    -   `data_loader.py`: Loads issues from the data file into runtime data structures.
    -   `model.py`: Defines the data models for issues and events.
    -   `config.py`: Manages configuration settings, allowing for easy customization.

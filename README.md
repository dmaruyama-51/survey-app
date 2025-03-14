# Survey Data Preprocessing App

## Description

This is a web application for efficiently preprocessing social survey data collected using Likert scales before subjecting them to statistical analysis. Specifically, it can perform everything from cleaning inappropriate responses to creating reversal items and calculating factor scores.  
Built with Streamlit and Python, the application offers intuitive, user-friendly tools for handling common data issues in survey research. The application is deployed on Google Cloud Run, ensuring scalability and ease of access for users.

The application is accessible at [here](https://survey-app-1037219502389.asia-northeast1.run.app/)


## Features

### Data Import Options
1. **Multiple File Formats**: Supports both CSV and Excel (.xlsx, .xls) file formats for data import.
2. **Sample Data**: Option to use built-in sample data for testing and demonstration.

### Data Cleaning Operations
1. **Straight-Line Response Removal**: Detects and removes responses where all answers have the same value.
2. **Missing Values Removal**: Removes rows with missing values to ensure data integrity.
3. **Out-of-Range Value Removal**: Filters out rows containing values outside the expected range (e.g., -1 or 100 in a 5-point scale).
4. **Sequential Pattern Detection**: Removes rows with sequential patterns (e.g., 1, 2, 3, 4, 5...).

### Data Manipulation Operations
1. **Reversal Items Creation**: Creates reverse-scored items with '_r' suffix while preserving original items.
2. **Factor Score Calculation**: 
   - Creates total scores and mean scores for multiple scales
   - Supports up to 10 different scales
   - Allows flexible item selection for each scale

### Data Visualization Operations
1. **Descriptive Statistics**: Calculates and displays key statistics (mean, median, standard deviation, etc.) for selected variables.
2. **Distribution Visualization**: Creates histograms to visualize the distribution of survey responses.
3. **Floor and Ceiling Effect Detection**: Automatically identifies variables that may suffer from floor or ceiling effects.

## Technical Stack

- Language: Python 3.11
- UI Framework: Streamlit 1.41.1
- Dependency Management: Poetry

## Development Setup

1. **Install Dependencies**:
   ```bash
   poetry install
   ```

2. **Run the Application**:
   ```bash
   make dev
   ```

3. **Linting and Formatting**:
   ```bash
   make lint
   make format
   ```

4. **Run Tests**:
   ```bash
   make test
   ```

### CI/CD
GitHub Actions are used for continuous integration and deployment:
- **PR Checks**: Runs tests, linting, and coverage checks on pull requests.
- **Deploy**: Deploys the latest changes to Artifact Regustrt and Cloud Run upon merging.

### Pre-requisites for Deployment

Before deploying via GitHub Actions, ensure the following environment variables and secrets are registered:

#### Environment Variables (GitHub Actions)
- `PROJECT_ID`: GCP Project ID.
- `REGION`: GCP Region.
- `REPOSITORY_NAME`: Artifact Registry repository name.
- `APP_NAME`: Cloud Run service name.

#### Secrets (GitHub Actions)
- `WORKLOAD_IDENTITY_PROVIDER`: Value for the Workload Identity Provider.
- `SERVICE_ACCOUNT`: Email address of the service account.

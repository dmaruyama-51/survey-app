# Survey Data Cleaning App

## Description

This is a web application designed to clean social survey data collected using Likert scales. Built with Streamlit and Python, the application offers intuitive, user-friendly tools for handling common data issues in survey research. The application is deployed on Google Cloud Run, ensuring scalability and ease of access for users.

## Features

### Data Cleaning Operations
1. **Straight-Line Response Removal**: Detects and removes responses where all answers have the same value.
2. **Missing Values Removal**: Removes rows with missing values to ensure data integrity.
3. **Out-of-Range Value Removal**: Filters out rows containing values outside the expected range (e.g., -1 or 100 in a 5-point scale).
4. **Sequential Pattern Detection**: Removes rows with sequential patterns (e.g., 1, 2, 3, 4, 5...).

### Technical Features
- **CSV File Upload**: Users can upload their survey data as a CSV file for cleaning.
- **Sample Data**: Sample datasets are available for testing the application.
- **Likert Scale Support**: Supports a wide range of Likert scale points (3-9).
- **Download Cleaned Data**: Enables users to download the cleaned data as a CSV file.

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

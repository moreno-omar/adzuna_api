# adzuna_api

A python module to make it easier to use Adzuna API. Can be used as a command-line tool or imported into other Python applications.

## Features

- Search for jobs using the Adzuna API
- Filter by job category, country, results per page, and salary range
- Command-line interface for interactive use
- CSV output with terminal preview (first 5 rows)
- Can be imported and used in other Python applications

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Basic search
adzuna

# Search for IT jobs in the US
adzuna --category it-jobs

# Search with salary filter
adzuna --min-salary 50000 --max-salary 100000

# Search in a different country
adzuna --country gb --category engineering-jobs

# Specify output file
adzuna --output my_jobs.csv

# Specify number of results per page
adzuna --results-per-page 100
```

### As a Python Module

```python
from adzuna_api import AdzunaClient

# Create client
client = AdzunaClient(app_id="your_app_id", app_key="your_app_key")

# Search for jobs
df = client.search_jobs(
    country="us",
    category="it-jobs",
    results_per_page=50,
    min_salary=50000,
    max_salary=100000
)

# Save to CSV
client.to_csv(df, "jobs.csv")

# Work with the DataFrame
print(df.head())
print(f"Found {len(df)} jobs")
```

## API Authentication

You can provide API credentials in two ways:

1. Command line options:
```bash
adzuna --app-id YOUR_APP_ID --app-key YOUR_APP_KEY
```

2. Environment variables:
```bash
export ADZUNA_APP_ID=YOUR_APP_ID
export ADZUNA_APP_KEY=YOUR_APP_KEY
adzuna
```

Note: The API may work without credentials for basic testing, but authentication is recommended for production use.

## Parameters

- `--country`: Country code (default: us). Examples: us, gb, ca, au, de, fr
- `--category`: Job category filter (e.g., 'it-jobs', 'engineering-jobs')
- `--results-per-page`: Number of results per page (default: 50)
- `--min-salary`: Minimum salary filter
- `--max-salary`: Maximum salary filter
- `--page`: Page number (default: 1)
- `--output`: Output CSV filename (default: adzuna_jobs.csv)

#!/usr/bin/env python3
"""Example usage of adzuna_api module

This script demonstrates how to use the adzuna_api module in your Python applications.
"""

from adzuna_api import AdzunaClient

# Example 1: Basic search
print("Example 1: Basic job search")
print("-" * 50)
client = AdzunaClient()

# Note: In a real scenario, you would provide app_id and app_key
# client = AdzunaClient(app_id="YOUR_APP_ID", app_key="YOUR_APP_KEY")

# Search for jobs
df = client.search_jobs(
    country="us",
    results_per_page=20
)

print(f"Found {len(df)} jobs")
if not df.empty:
    print("\nFirst few results:")
    print(df.head())

# Example 2: Search with filters
print("\n\nExample 2: Search with filters")
print("-" * 50)
df = client.search_jobs(
    country="us",
    category="it-jobs",
    results_per_page=10,
    min_salary=50000,
    max_salary=100000
)

print(f"Found {len(df)} IT jobs with salary between $50,000 and $100,000")

# Example 3: Save results to CSV
print("\n\nExample 3: Save to CSV")
print("-" * 50)
if not df.empty:
    output_file = client.to_csv(df, "example_jobs.csv")
    print(f"Results saved to: {output_file}")

# Example 4: Work with the DataFrame
print("\n\nExample 4: Analyze the data")
print("-" * 50)
if not df.empty and 'salary_min' in df.columns:
    print(f"Average minimum salary: ${df['salary_min'].mean():,.2f}")
    if 'salary_max' in df.columns:
        print(f"Average maximum salary: ${df['salary_max'].mean():,.2f}")
    
    if 'category_name' in df.columns:
        print("\nJob categories found:")
        print(df['category_name'].value_counts())

print("\n" + "=" * 50)
print("For more information, run: adzuna --help")

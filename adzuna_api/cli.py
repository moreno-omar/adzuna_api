"""CLI interface for Adzuna API

Command-line interface for searching jobs using the Adzuna API.
"""

import click
import os
from .client import AdzunaClient


@click.command()
@click.option(
    "--country",
    default="us",
    help="Country code (e.g., us, gb, ca, au, de, fr)",
    show_default=True,
)
@click.option(
    "--category",
    help="Job category filter (e.g., 'it-jobs', 'engineering-jobs')",
)
@click.option(
    "--results-per-page",
    default=50,
    type=int,
    help="Number of results per page",
    show_default=True,
)
@click.option(
    "--min-salary",
    type=float,
    help="Minimum salary filter",
)
@click.option(
    "--max-salary",
    type=float,
    help="Maximum salary filter",
)
@click.option(
    "--page",
    default=1,
    type=int,
    help="Page number",
    show_default=True,
)
@click.option(
    "--output",
    default="adzuna_jobs.csv",
    help="Output CSV filename",
    show_default=True,
)
@click.option(
    "--app-id",
    envvar="ADZUNA_APP_ID",
    help="Adzuna API application ID (or set ADZUNA_APP_ID env var)",
)
@click.option(
    "--app-key",
    envvar="ADZUNA_APP_KEY",
    help="Adzuna API application key (or set ADZUNA_APP_KEY env var)",
)
def main(country, category, results_per_page, min_salary, max_salary, page, output, app_id, app_key):
    """Search for jobs using the Adzuna API.
    
    By default, outputs results to a CSV file and displays the first 5 rows in the terminal.
    
    Examples:
    
        # Search for IT jobs in the US
        adzuna --category it-jobs
        
        # Search for jobs with salary filter
        adzuna --min-salary 50000 --max-salary 100000
        
        # Search in a different country
        adzuna --country gb --category engineering-jobs
    """
    # Create client
    client = AdzunaClient(app_id=app_id, app_key=app_key)
    
    # Build search parameters
    search_params = {
        "country": country,
        "results_per_page": results_per_page,
        "page": page,
    }
    
    if category:
        search_params["category"] = category
    
    if min_salary is not None:
        search_params["min_salary"] = min_salary
    
    if max_salary is not None:
        search_params["max_salary"] = max_salary
    
    # Display search parameters
    click.echo("Searching for jobs with parameters:")
    for key, value in search_params.items():
        click.echo(f"  {key}: {value}")
    click.echo()
    
    # Search for jobs
    df = client.search_jobs(**search_params)
    
    if df.empty:
        click.echo("No jobs found matching your criteria.")
        return
    
    # Save to CSV
    client.to_csv(df, output)
    click.echo(f"Results saved to: {output}")
    click.echo(f"Total jobs found: {len(df)}")
    click.echo()
    
    # Display first 5 rows in terminal
    click.echo("First 5 results:")
    click.echo("-" * 80)
    
    # Display the first 5 rows
    display_df = df.head(5)
    
    # Format the output for terminal display
    for idx, row in display_df.iterrows():
        click.echo(f"\nJob {idx + 1}:")
        for col in display_df.columns:
            value = row[col]
            # Truncate long values
            if isinstance(value, str) and len(value) > 100:
                value = value[:97] + "..."
            click.echo(f"  {col}: {value}")
    
    click.echo()
    click.echo("-" * 80)
    click.echo(f"Showing 5 of {len(df)} total results. See {output} for all results.")


if __name__ == "__main__":
    main()

"""Adzuna API Client

Core client for interacting with the Adzuna API.
"""

import requests
from typing import Optional, Dict, Any, List
import pandas as pd


class AdzunaClient:
    """Client for interacting with the Adzuna API"""
    
    BASE_URL = "https://api.adzuna.com/v1/api"
    
    def __init__(self, app_id: Optional[str] = None, app_key: Optional[str] = None):
        """Initialize the Adzuna API client
        
        Args:
            app_id: Adzuna API application ID
            app_key: Adzuna API application key
        """
        self.app_id = app_id
        self.app_key = app_key
    
    def search_jobs(
        self,
        country: str = "us",
        category: Optional[str] = None,
        results_per_page: int = 50,
        page: int = 1,
        min_salary: Optional[float] = None,
        max_salary: Optional[float] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Search for jobs using the Adzuna API
        
        Args:
            country: Country code (e.g., 'us', 'gb', 'ca')
            category: Job category filter
            results_per_page: Number of results per page
            page: Page number
            min_salary: Minimum salary filter
            max_salary: Maximum salary filter
            **kwargs: Additional parameters to pass to the API
        
        Returns:
            DataFrame containing job search results
        """
        # Build the API endpoint URL
        endpoint = f"{self.BASE_URL}/jobs/{country}/search/{page}"
        
        # Build query parameters
        params: Dict[str, Any] = {
            "results_per_page": results_per_page,
        }
        
        # Add authentication if provided
        if self.app_id and self.app_key:
            params["app_id"] = self.app_id
            params["app_key"] = self.app_key
        
        # Add optional filters
        if category:
            params["category"] = category
        
        if min_salary is not None:
            params["salary_min"] = min_salary
        
        if max_salary is not None:
            params["salary_max"] = max_salary
        
        # Add any additional parameters
        params.update(kwargs)
        
        # Make the API request
        try:
            response = requests.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Extract results
            results = data.get("results", [])
            
            if not results:
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(results)

            # Select and normalize useful columns
            return self._select_columns(df)
            
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error processing API response: {e}")
            return pd.DataFrame()
    
    def to_csv(self, df: pd.DataFrame, filename: str = "adzuna_jobs.csv") -> str:
        """Save DataFrame to CSV file
        
        Args:
            df: DataFrame to save
            filename: Output filename
        
        Returns:
            Path to the saved file
        """
        df.to_csv(filename, index=False)
        return filename

    def _select_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Select and normalize useful columns from job search results."""
        normalized = pd.json_normalize(df.to_dict(orient="records"))
        columns_to_keep = [
            "title",
            "company.display_name",
            "location.display_name",
            "category.label",
            "salary_min",
            "salary_max",
            "description",
            "redirect_url",
        ]
        return normalized[columns_to_keep]



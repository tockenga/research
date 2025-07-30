"""Literature review search string generator package.

This package provides tools to generate search strings for various academic databases
including IEEE, ACM, EBSCO, and ScienceDirect.
"""

from .generator import SearchStringGenerator
from .database_configs import DatabaseConfig, IEEE_CONFIG, ACM_CONFIG, EBSCO_CONFIG, SCIENCEDIRECT_CONFIG
from .query_builder import QueryBuilder

__version__ = "1.0.0"
__all__ = [
    "SearchStringGenerator",
    "DatabaseConfig", 
    "IEEE_CONFIG",
    "ACM_CONFIG", 
    "EBSCO_CONFIG",
    "SCIENCEDIRECT_CONFIG",
    "QueryBuilder"
]
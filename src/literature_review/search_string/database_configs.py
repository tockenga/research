"""Database configuration settings for different academic search engines."""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class DatabaseConfig:
    """Configuration for a specific academic database."""
    
    name: str
    url: str
    title_field: str
    abstract_field: str
    keywords_field: str
    instructions: Optional[str] = None
    
    def get_field_mapping(self) -> Dict[str, str]:
        """Get the field mapping for this database."""
        return {
            'title': self.title_field,
            'abstract': self.abstract_field,
            'keywords': self.keywords_field
        }


# IEEE Xplore configuration
IEEE_CONFIG = DatabaseConfig(
    name="IEEE Xplore",
    url="https://ieeexplore.ieee.org/search/advanced/command",
    title_field='"Document Title":',
    abstract_field='"Abstract":',
    keywords_field='"Author Keywords":',
    instructions="Maximum of 25 search terms per search clause."
)

# ACM Digital Library configuration
ACM_CONFIG = DatabaseConfig(
    name="ACM Digital Library", 
    url="https://dl.acm.org/search/advanced",
    title_field='Title:',
    abstract_field='Abstract:',
    keywords_field='',  # Keywords handled differently in ACM
    instructions='Choose "Author Keyword" in the "Search Within" dropdown menu and insert the following string:'
)

# EBSCO configuration
EBSCO_CONFIG = DatabaseConfig(
    name="EBSCO",
    url="https://research.ebsco.com/c/fi3tnl/search/advanced/filters?limiters=None",
    title_field='TI',
    abstract_field='AB', 
    keywords_field='SU',
    instructions='Login with your institution to use the database. Then insert string in the advanced search box under all fields.'
)

# ScienceDirect configuration (simplified approach)
SCIENCEDIRECT_CONFIG = DatabaseConfig(
    name="ScienceDirect",
    url="https://www.sciencedirect.com/search",
    title_field='',  # Uses simplified syntax
    abstract_field='',
    keywords_field='',
    instructions='Insert in "Title, abstract or author-specified keywords"'
)
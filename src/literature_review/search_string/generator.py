"""Main search string generator for literature reviews."""

from typing import List, Dict, Any, Optional
from .database_configs import DatabaseConfig, IEEE_CONFIG, ACM_CONFIG, EBSCO_CONFIG, SCIENCEDIRECT_CONFIG
from .query_builder import QueryBuilder


class SearchStringGenerator:
    """Generates search strings for academic literature review across multiple databases."""
    
    def __init__(self):
        """Initialize the generator with default database configurations."""
        self.databases = {
            'ieee': IEEE_CONFIG,
            'acm': ACM_CONFIG, 
            'ebsco': EBSCO_CONFIG,
            'sciencedirect': SCIENCEDIRECT_CONFIG
        }
    
    def generate_queries_from_terms(self, search_terms: List[List[str]]) -> List[Dict[str, List[str]]]:
        """Generate query structures from grouped search terms.
        
        Terms within each group will be connected with OR operators.
        Groups will be connected with AND operators.
        
        Args:
            search_terms: List of term groups, where each group is a list of related terms
            
        Returns:
            List of query dictionaries suitable for database search
            
        Example:
            >>> generator = SearchStringGenerator()
            >>> terms = [['cryptocurrency', 'bitcoin'], ['returns'], ['prediction', 'forecast']]
            >>> queries = generator.generate_queries_from_terms(terms)
        """
        queries = []
        
        for term_group in search_terms:
            # Each term group gets applied to title, abstract, and keywords fields
            query = {
                'title': term_group.copy(),
                'abstract': term_group.copy(), 
                'keywords': term_group.copy()
            }
            queries.append(query)
            
        return queries
    
    def generate_for_database(self, database_key: str, search_terms: List[List[str]]) -> Dict[str, Any]:
        """Generate a search string for a specific database.
        
        Args:
            database_key: Key identifying the database ('ieee', 'acm', 'ebsco', 'sciencedirect')
            search_terms: List of term groups for the search
            
        Returns:
            Dictionary containing the search string and metadata
            
        Raises:
            ValueError: If database_key is not recognized
        """
        if database_key not in self.databases:
            available = ', '.join(self.databases.keys())
            raise ValueError(f"Unknown database '{database_key}'. Available: {available}")
        
        config = self.databases[database_key]
        builder = QueryBuilder(config)
        queries = self.generate_queries_from_terms(search_terms)
        search_string = builder.build_query(queries)
        
        return {
            'database': config.name,
            'url': config.url,
            'search_string': search_string,
            'instructions': config.instructions,
            'term_count': sum(len(group) for group in search_terms),
            'group_count': len(search_terms)
        }
    
    def generate_all(self, search_terms: List[List[str]]) -> Dict[str, Dict[str, Any]]:
        """Generate search strings for all configured databases.
        
        Args:
            search_terms: List of term groups for the search
            
        Returns:
            Dictionary mapping database keys to search results
        """
        results = {}
        
        for db_key in self.databases:
            results[db_key] = self.generate_for_database(db_key, search_terms)
            
        return results
    
    def format_output(self, database_key: str, search_terms: List[List[str]]) -> str:
        """Generate formatted output for a specific database (matching notebook style).
        
        Args:
            database_key: Key identifying the database
            search_terms: List of term groups for the search
            
        Returns:
            Formatted string ready for copy-paste
        """
        result = self.generate_for_database(database_key, search_terms)
        
        output = [f"{result['url']}"]
        
        if result['instructions']:
            output.append(result['instructions'])
            
        output.append(result['search_string'])
        
        return '\n'.join(output)
    
    def print_all_results(self, search_terms: List[List[str]]) -> None:
        """Print formatted results for all databases (matching notebook output).
        
        Args:
            search_terms: List of term groups for the search
        """
        results = self.generate_all(search_terms)
        
        # Print in the same order as the notebook
        database_order = ['ieee', 'acm', 'sciencedirect', 'ebsco']
        
        for i, db_key in enumerate(database_order):
            if i > 0:
                print()  # Add blank line between databases
                
            config = self.databases[db_key]
            print(f"## {config.name}")
            
            if config.instructions:
                if config.name == "IEEE Xplore":
                    print("There is a maximum of 25 search terms per search clause.")
                    
            print(self.format_output(db_key, search_terms))
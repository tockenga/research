"""Query building logic for academic search strings."""

from typing import List, Dict, Any
from .database_configs import DatabaseConfig


class QueryBuilder:
    """Builds search query strings for academic databases."""
    
    def __init__(self, config: DatabaseConfig):
        """Initialize with a database configuration.
        
        Args:
            config: Database configuration specifying field formats
        """
        self.config = config
        self.field_mapping = config.get_field_mapping()
    
    def append_terms_for_field(self, field: str, elements: List[str], operator: str = 'OR') -> str:
        """Combine search terms for a specific field with the given operator.
        
        Args:
            field: The database field identifier (e.g., 'TI', '"Document Title":')
            elements: List of search terms
            operator: Operator to use between terms (default: 'OR')
            
        Returns:
            Formatted search string for the field
        """
        if not elements:
            return ""
            
        result = ""
        last_index = len(elements) - 1
        
        for index, element in enumerate(elements):
            if field:  # Some databases use field prefixes
                term = f'({field} {element})'
            else:  # Others use plain terms
                term = element
                
            if index != last_index:
                result += f'{term} {operator} '
            else:
                result += term
                
        return result
    
    def construct_standard_query(self, queries: List[Dict[str, List[str]]], operator: str = 'AND') -> str:
        """Construct a standard query for databases with field prefixes.
        
        Args:
            queries: List of query dictionaries with field->terms mappings
            operator: Operator between query groups (default: 'AND')
            
        Returns:
            Complete formatted search string
        """
        result = ''
        last_index = len(queries) - 1
        
        for index, query in enumerate(queries):
            sub_query = []
            
            for field_type, elements in query.items():
                if field_type in self.field_mapping and elements:
                    field = self.field_mapping[field_type]
                    sub_query.append(self.append_terms_for_field(field, elements))
            
            if sub_query:
                query_part = f'({" OR ".join(sub_query)})'
                if index != last_index:
                    result += f'{query_part} {operator} '
                else:
                    result += query_part
                    
        return result
    
    def construct_simple_query(self, queries: List[Dict[str, List[str]]]) -> str:
        """Construct a simplified query for databases like ScienceDirect.
        
        Args:
            queries: List of query dictionaries with field->terms mappings
            
        Returns:
            Simplified search string
        """
        result = []
        
        for query in queries:
            # Combine all terms from all fields (eliminating duplicates)
            all_terms = set()
            for field_type, elements in query.items():
                if elements:
                    all_terms.update(elements)
            
            if all_terms:
                # Sort for consistent output
                terms = sorted(list(all_terms))
                result.append(f"({' OR '.join(terms)})")
        
        return ' AND '.join(result)
    
    def build_query(self, queries: List[Dict[str, List[str]]]) -> str:
        """Build a search query appropriate for the configured database.
        
        Args:
            queries: List of query dictionaries with field->terms mappings
            
        Returns:
            Formatted search string for the database
        """
        if self.config.name == "ScienceDirect":
            return self.construct_simple_query(queries)
        else:
            query = self.construct_standard_query(queries)
            
            # Special handling for ACM (remove extra spaces)
            if self.config.name == "ACM Digital Library":
                query = query.replace('( ', '(')
                
            return query
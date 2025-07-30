"""Command line interface for the search string generator."""

import argparse
import json
import sys
from typing import List
from .generator import SearchStringGenerator


def parse_search_terms(terms_input: str) -> List[List[str]]:
    """Parse search terms from command line input.
    
    Supports multiple formats:
    - JSON: '[["crypto", "bitcoin"], ["returns"], ["prediction"]]'
    - Semicolon groups: 'crypto,bitcoin;returns;prediction,forecast'
    
    Args:
        terms_input: String representation of search terms
        
    Returns:
        Parsed search terms as list of lists
    """
    terms_input = terms_input.strip()
    
    # Try JSON format first
    if terms_input.startswith('['):
        try:
            return json.loads(terms_input)
        except json.JSONDecodeError:
            pass
    
    # Try semicolon-separated groups format
    if ';' in terms_input:
        groups = []
        for group in terms_input.split(';'):
            group = group.strip()
            if group:
                terms = [term.strip() for term in group.split(',') if term.strip()]
                if terms:
                    groups.append(terms)
        return groups
    
    # Single group, comma-separated
    terms = [term.strip() for term in terms_input.split(',') if term.strip()]
    return [terms] if terms else []


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate academic search strings for literature reviews',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate for all databases with JSON format
  %(prog)s '[["cryptocurrency", "bitcoin"], ["returns"], ["prediction", "forecast"]]'
  
  # Generate for specific database with semicolon format  
  %(prog)s -d ieee 'crypto,bitcoin;returns;prediction,forecast'
  
  # Generate for ACM with comma-separated single group
  %(prog)s -d acm 'machine learning,deep learning,neural networks'
        """
    )
    
    parser.add_argument(
        'search_terms',
        help='Search terms in JSON format or semicolon-separated groups'
    )
    
    parser.add_argument(
        '-d', '--database',
        choices=['ieee', 'acm', 'ebsco', 'sciencedirect', 'all'],
        default='all',
        help='Target database (default: all)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true', 
        help='Show statistics about the search terms'
    )
    
    args = parser.parse_args()
    
    try:
        search_terms = parse_search_terms(args.search_terms)
        if not search_terms:
            print("Error: No valid search terms provided", file=sys.stderr)
            return 1
            
        generator = SearchStringGenerator()
        
        if args.stats:
            total_terms = sum(len(group) for group in search_terms)
            print(f"Search term statistics:")
            print(f"  Groups: {len(search_terms)}")
            print(f"  Total terms: {total_terms}")
            print(f"  Terms per group: {[len(group) for group in search_terms]}")
            print()
        
        if args.database == 'all':
            if args.json:
                results = generator.generate_all(search_terms)
                print(json.dumps(results, indent=2))
            else:
                generator.print_all_results(search_terms)
        else:
            if args.json:
                result = generator.generate_for_database(args.database, search_terms)
                print(json.dumps(result, indent=2))
            else:
                print(generator.format_output(args.database, search_terms))
                
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1
        
    return 0


if __name__ == '__main__':
    sys.exit(main())
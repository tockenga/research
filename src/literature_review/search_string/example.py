"""Example usage of the search string generator (replicating notebook results)."""

from .generator import SearchStringGenerator


def main():
    """Run example that should match the notebook output."""
    
    # Same search terms as in the notebook
    search_terms = [
        ['cryptocurrency', 'ethereum', 'bitcoin'], 
        ['returns'], 
        ['prediction', 'predict', 'predicting', 'forecast']
    ]
    
    print("=== Literature Review Search String Generator ===")
    print(f"Search terms: {search_terms}")
    print("\nTerms within groups will be connected with OR operators")
    print("Groups will be connected with AND operators")
    print("\n" + "="*60 + "\n")
    
    generator = SearchStringGenerator()
    generator.print_all_results(search_terms)


if __name__ == '__main__':
    main()
# Literature Review Search String Generator

A Python package for generating academic search strings across multiple databases for systematic literature reviews.

## Overview

This package converts grouped search terms into properly formatted search strings for different academic databases including IEEE Xplore, ACM Digital Library, EBSCO, and ScienceDirect.

## Features

- **Multi-database support**: Generate search strings for IEEE, ACM, EBSCO, and ScienceDirect
- **Flexible input formats**: Support for JSON and semicolon-separated term groups
- **Command-line interface**: Easy-to-use CLI for quick generation
- **Programmatic API**: Use as a Python library in your own scripts
- **Proper formatting**: Database-specific syntax and field mappings

## Installation

Since this is part of the research project, install it by adding the project root to your Python path:

```bash
# From the project root directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## Quick Start

### Command Line Usage

```bash
# Generate for all databases
python -m src.literature_review.search_string.cli '[["cryptocurrency", "bitcoin"], ["returns"], ["prediction", "forecast"]]'

# Generate for specific database
python -m src.literature_review.search_string.cli -d ieee 'crypto,bitcoin;returns;prediction,forecast'

# Show statistics
python -m src.literature_review.search_string.cli --stats 'machine learning,AI;classification;prediction'

# JSON output
python -m src.literature_review.search_string.cli --json -d acm 'neural networks;deep learning'
```

### Python API Usage

```python
from src.literature_review.search_string import SearchStringGenerator

# Initialize generator
generator = SearchStringGenerator()

# Define search terms (groups will be AND-ed, terms within groups will be OR-ed)
search_terms = [
    ['cryptocurrency', 'ethereum', 'bitcoin'],  # Group 1: crypto terms
    ['returns'],                                 # Group 2: returns
    ['prediction', 'predict', 'forecast']       # Group 3: prediction terms
]

# Generate for all databases
results = generator.generate_all(search_terms)

# Generate for specific database
ieee_result = generator.generate_for_database('ieee', search_terms)

# Print formatted output (matches original notebook style)
generator.print_all_results(search_terms)
```

## Input Formats

### JSON Format

```bash
'[["term1", "term2"], ["term3"], ["term4", "term5"]]'
```

### Semicolon-separated Groups

```bash
'term1,term2;term3;term4,term5'
```

### Single Group (comma-separated)

```bash
'term1,term2,term3'
```

## Supported Databases

| Database            | Key             | Field Syntax                                             |
| ------------------- | --------------- | -------------------------------------------------------- |
| IEEE Xplore         | `ieee`          | `"Document Title":`, `"Abstract":`, `"Author Keywords":` |
| ACM Digital Library | `acm`           | `Title:`, `Abstract:`, plus plain keywords               |
| EBSCO               | `ebsco`         | `TI`, `AB`, `SU`                                         |
| ScienceDirect       | `sciencedirect` | Simplified syntax (terms only)                           |

## Example Output

For search terms `[["cryptocurrency", "bitcoin"], ["returns"], ["prediction"]]`:

**IEEE Xplore:**

```
(("Document Title": cryptocurrency) OR ("Document Title": bitcoin) OR
("Abstract": cryptocurrency) OR ("Abstract": bitcoin) OR
("Author Keywords": cryptocurrency) OR ("Author Keywords": bitcoin)) AND
(("Document Title": returns) OR ("Abstract": returns) OR ("Author Keywords": returns)) AND
(("Document Title": prediction) OR ("Abstract": prediction) OR ("Author Keywords": prediction))
```

**ScienceDirect:**

```
(bitcoin OR cryptocurrency) AND (returns) AND (prediction)
```

## Package Structure

```
src/literature_review/search_string/
├── __init__.py              # Package exports
├── database_configs.py      # Database configuration classes
├── query_builder.py         # Core query building logic
├── generator.py             # Main SearchStringGenerator class
├── cli.py                   # Command line interface
├── example.py               # Example usage (replicates notebook)
└── README.md               # This file
```

## API Reference

### SearchStringGenerator

Main class for generating search strings.

#### Methods

- `generate_queries_from_terms(search_terms)`: Convert term groups to query format
- `generate_for_database(database_key, search_terms)`: Generate for specific database
- `generate_all(search_terms)`: Generate for all databases
- `format_output(database_key, search_terms)`: Get formatted string output
- `print_all_results(search_terms)`: Print all results (notebook style)

### DatabaseConfig

Configuration class for database-specific settings.

#### Attributes

- `name`: Database display name
- `url`: Database search URL
- `title_field`: Field syntax for title searches
- `abstract_field`: Field syntax for abstract searches
- `keywords_field`: Field syntax for keyword searches
- `instructions`: Special instructions for the database

## Migration from Notebook

This package replicates and extends the functionality from the original Jupyter notebook:

- All database configurations are preserved
- Query building logic matches exactly
- Output format is identical
- Additional features: CLI, JSON output, flexible input formats

## Contributing

To extend support for additional databases:

1. Add a new `DatabaseConfig` in `database_configs.py`
2. Update the `SearchStringGenerator.databases` dict
3. Add any special handling in `QueryBuilder` if needed

## License

Part of the research project - see main project license.

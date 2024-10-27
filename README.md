# JSONDetective

A powerful tool for analyzing JSON structures and generating Python dataclasses.

## Installation

```bash
pip install jsondetective
```

## Usage

### Command Line

Analyze a JSON file:
```bash
jsondetective --json-path data.json
```

Generate a Python dataclass:
```bash
jsondetective --json-path data.json --create-dataclass
```

Save the dataclass to a file:
```bash
jsondetective --json-path data.json --create-dataclass --output-path my_dataclass.py
```

### Python Library

```python
from jsondetective import JSONSchemaAnalyzer

# Initialize analyzer
analyzer = JSONSchemaAnalyzer()

# Analyze JSON file
analyzer.analyze_file("data.json")

# Print schema
analyzer.print_schema()

# Generate dataclass code
schema = analyzer._build_nested_schema()
analyzer.schema_to_dataclass_file(schema, "output.py", "MyDataClass")
```

## Features

- Analyzes JSON structure and infers schema
- Detects optional fields
- Generates Python dataclasses with proper type hints
- Handles nested structures and arrays
- Supports both command-line and library usage

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
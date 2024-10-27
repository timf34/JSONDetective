# JSONDetective 🔍

A powerful tool for analyzing and understanding JSON schemas, especially useful for large and complex JSON files.

## Quick Start

```bash
# Install
pip install jsondetective

# Use
jsondetective data.json
```

## What Does It Do?

Given a complex JSON file like:

```json
{
  "users": [
    {
      "id": "123",
      "joined_date": "2024-01-15",
      "last_active": "2024-03-20T15:30:00Z",
      "stats": {
        "posts": 42,
        "likes_received": 156
      },
      "preferences": {
        "theme": "dark",
        "notifications": true
      }
    },
    // ... many more users
  ]
}
```

JSONDetective will produce a clean schema like:

```json
{
  "users": {
    "type": "array",
    "items": {
      "id": {
        "type": "string",
        "examples": ["123"]
      },
      "joined_date": {
        "type": "string",
        "format": "yyyy-mm-dd"
      },
      "last_active": {
        "type": "string",
        "format": "datetime"
      },
      "stats": {
        "type": "object",
        "properties": {
          "posts": {
            "type": "integer"
          },
          "likes_received": {
            "type": "integer"
          }
        }
      },
      "preferences": {
        "type": "object",
        "properties": {
          "theme": {
            "type": "string",
            "optional": true
          },
          "notifications": {
            "type": "boolean"
          }
        }
      }
    }
  }
}
```

## Features

- **Schema Inference**: Automatically detects and analyzes JSON structure
- **Smart Pattern Recognition**: 
  - Identifies and normalizes date patterns
  - Detects optional fields
  - Abstracts repeated patterns into clear structures
- **Intuitive Visualization**: Clean, readable output of your JSON schema
- **Experimental Dataclass Generation**: Convert JSON schemas to Python dataclasses (beta feature)

## Advanced Usage

### Experimental Python Dataclass Generation

```bash
# Print dataclass to console
jsondetective data.json -d

# Save to file
jsondetective data.json -d -o my_dataclasses.py

# Custom class name
jsondetective data.json -d -c MyDataClass
```

### CLI Options

```bash
jsondetective [JSON_FILE] [OPTIONS]

Options:
  -d, --create-dataclass     Generate Python dataclass code
  -o, --output-path PATH     Save dataclass to file
  -c, --class-name TEXT      Name for the root dataclass (default: Root)
  --help                     Show this message and exit
```

## Why JSONDetective?

- **Large JSON Files**: Quickly understand the structure of large JSON files without having to manually inspect them
- **Pattern Detection**: Automatically identifies and normalizes common patterns like dates
- **Optional Fields**: Clearly shows which fields are optional by analyzing multiple instances
- **Sample Values**: Provides example values while maintaining a clean schema view
- **Date Pattern Recognition**: Automatically detects and normalizes various date formats

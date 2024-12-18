﻿# JSONDetective 🔍

A powerful tool for analyzing and understanding JSON schemas. Built to handle large, complex JSON files by
automatically detecting and abstracting patterns in your data.

Key features:
- Automatically recognizes and normalizes date formats in both keys and values
- Detects optional fields by analyzing multiple instances
- Abstracts repeated patterns into clean, readable schemas

## Quick Start

```bash
# Install
pip install jsondetective

# Use
jsondetective data.json
```

## Pattern Recognition Example

Given a JSON with repeated date patterns like:
```json
{
  "2021-08-24": {"views": 100, "likes": 20},
  "2021-08-25": {"views": 150, "likes": 30},
  "2021-08-26": {"views": 200, "likes": 40}
}
```

JSONDetective recognizes the pattern and abstracts it as:
```json
{
  "yyyy-mm-dd_1": {
    "type": "object",
    "properties": {
      "views": {"type": "integer"},
      "likes": {"type": "integer"}
    }
  }
}
```
Note: The `_1` suffix indicates the nesting level in the JSON structure.

## Complex Structure Example

It also handles nested structures with various data types and patterns:

```json
{
  "users": [
    {
      "id": "123",
      "joined_date": "2024-01-15",
      "last_active": "2024-03-20T15:30:00Z",
      "activity": {
        "2024-03-19": {"posts": 5},
        "2024-03-20": {"posts": 3}
      },
      "preferences": {
        "theme": "dark",
        "notifications": true
      }
    }
  ],
  // many more users...
}
```

Produces this clean schema:
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
      "activity": {
        "type": "object",
        "properties": {
          "yyyy-mm-dd_2": {
            "type": "object",
            "properties": {
              "posts": {"type": "integer"}
            }
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

- **Intelligent Pattern Detection**: 
  - Recognizes date formats in both keys and values
  - Abstracts repeated structures
  - Identifies optional fields
- **Schema Intelligence**: 
  - Detects data types
  - Identifies nested structures
  - Provides example values
- **Experimental**: Python dataclass generation (beta feature)

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

## Why Use JSONDetective?

- **Pattern Recognition**: Automatically detects and abstracts repeated patterns
- **Date Handling**: Intelligent date format recognition and normalization
- **Large Files**: Efficiently processes and summarizes large JSON structures
- **Clear Output**: Clean, readable schema representation
- **Time Saving**: No manual inspection of large JSON files needed

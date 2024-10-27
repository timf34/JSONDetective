import json
from collections import defaultdict
from typing import Dict, Any, Union, Tuple, TextIO
from datetime import datetime
from rich.console import Console
from rich.syntax import Syntax


class JSONSchemaAnalyzer:
    """Analyzes JSON structures to infer schema and generate dataclasses."""

    def __init__(self):
        self.schema_structure = {}
        self.max_unique_samples = 5
        self.date_counters = defaultdict(int)
        self.field_occurrence = defaultdict(int)
        self.total_objects_analyzed = 0

    @staticmethod
    def load_json(file_or_path: Union[str, TextIO]) -> Any:
        """Load JSON from a file path or file object."""
        try:
            if isinstance(file_or_path, str):
                with open(file_or_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return json.load(file_or_path)
        except UnicodeDecodeError:
            # Try alternative encodings
            encodings = ['utf-8-sig', 'latin-1']
            for encoding in encodings:
                try:
                    if isinstance(file_or_path, str):
                        with open(file_or_path, 'r', encoding=encoding) as f:
                            return json.load(f)
                    file_or_path.seek(0)  # Reset file pointer
                    return json.load(file_or_path, encoding=encoding)
                except:
                    continue
            raise ValueError("Unable to decode JSON file with supported encodings")

    @staticmethod
    def _get_type_name(value: Any) -> str:
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int):
            return 'integer'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, str):
            return 'string'
        elif isinstance(value, list):
            return 'array'
        elif isinstance(value, dict):
            return 'object'
        return str(type(value).__name__)

    def _detect_date_pattern(self, key: str) -> Tuple[bool, str]:
        """Check if a string is a date and return its pattern format."""
        date_patterns = {
            '%Y-%m-%d': 'yyyy-mm-dd',  # 2021-11-08
            '%d-%m-%Y': 'dd-mm-yyyy',  # 08-11-2021
            '%Y/%m/%d': 'yyyy/mm/dd',  # 2021/11/08
            '%d/%m/%Y': 'dd/mm/yyyy',  # 08/11/2021
            '%Y%m%d': 'yyyymmdd',  # 20211108
            '%d%m%Y': 'ddmmyyyy',  # 08112021
            '%B %d, %Y': 'month dd, yyyy',  # November 08, 2021
            '%d %B %Y': 'dd month yyyy',  # 08 November 2021
            '%Y-%m': 'yyyy-mm',  # 2021-11
            '%m-%Y': 'mm-yyyy',  # 11-2021
        }

        for strftime_pattern, readable_pattern in date_patterns.items():
            try:
                datetime.strptime(key, strftime_pattern)
                return True, readable_pattern
            except ValueError:
                continue
        return False, ''

    def _normalize_path(self, path: str) -> str:
        """Convert date-based keys to a normalized format with pattern."""
        if not path:
            return path

        parts = path.split('.')
        normalized_parts = []

        for part in parts:
            is_date, pattern = self._detect_date_pattern(part)
            if is_date:
                level = len(normalized_parts)
                date_key = f"{pattern}_{level}"
                normalized_parts.append(date_key)
            else:
                normalized_parts.append(part)

        return '.'.join(normalized_parts)

    def _analyze_value(self, path: str, value: Any) -> None:
        """Recursively analyze a value and update statistics."""
        normalized_path = self._normalize_path(path)
        value_type = self._get_type_name(value)

        # Increment occurrence counter for this path
        self.field_occurrence[normalized_path] += 1

        if normalized_path not in self.schema_structure:
            self.schema_structure[normalized_path] = {
                'type': value_type,
                'samples': set()
            }

        if not isinstance(value, (dict, list)) and len(
                self.schema_structure[normalized_path]['samples']) < self.max_unique_samples:
            self.schema_structure[normalized_path]['samples'].add(str(value))

        if isinstance(value, dict):
            for key, val in value.items():
                new_path = f"{path}.{key}" if path else key
                self._analyze_value(new_path, val)
        elif isinstance(value, list) and value:
            self._analyze_value(f"{normalized_path}[]", value[0])

    def analyze_json(self, json_data: Union[Dict, list]) -> None:
        """Analyze multiple objects from the JSON data."""
        if isinstance(json_data, list):
            # Analyze up to first 3 objects
            for i, record in enumerate(json_data[:3]):
                self._analyze_value("", record)
                self.total_objects_analyzed += 1
        else:
            # If it's a dictionary, analyze up to first 3 values
            for i, (_, record) in enumerate(list(json_data.items())[:3]):
                self._analyze_value("", record)
                self.total_objects_analyzed += 1

    def _merge_schema_objects(self, obj1: Dict, obj2: Dict) -> Dict:
        """Merge two schema objects, properly handling arrays and nested objects."""
        if not isinstance(obj1, dict) or not isinstance(obj2, dict):
            return obj1

        result = obj1.copy()

        # Special handling for 'items' in arrays
        if 'type' in result and result['type'] == 'array' and 'items' in result and 'items' in obj2:
            if isinstance(result['items'], dict) and isinstance(obj2['items'], dict):
                result['items'] = self._merge_schema_objects(result['items'], obj2['items'])
            return result

        # Special handling for 'properties' in objects
        if 'properties' in result and 'properties' in obj2:
            result['properties'] = self._merge_schema_objects(result['properties'], obj2['properties'])
            return result

        # Merge other keys
        for key, value in obj2.items():
            if key not in result:
                result[key] = value
            elif isinstance(value, dict) and isinstance(result[key], dict):
                result[key] = self._merge_schema_objects(result[key], value)

        return result

    def _build_nested_schema(self) -> Dict:
        """Convert flat schema structure to nested dictionary."""

        def create_nested_dict(path_parts: list, value: Dict, full_path: str) -> Dict:
            if not path_parts:
                result = {'type': value['type']}
                if value['samples']:
                    result['examples'] = list(value['samples'])
                # Add required/optional status based on field occurrence
                if self.field_occurrence[full_path] < self.total_objects_analyzed:
                    result['optional'] = True
                return result

            current_part = path_parts[0]
            remaining_parts = path_parts[1:]

            if current_part.endswith('[]'):
                current_part = current_part[:-2]
                return {
                    current_part: {
                        'type': 'array',
                        'items': create_nested_dict(remaining_parts, value, full_path)
                    }
                }
            else:
                nested = create_nested_dict(remaining_parts, value, full_path)
                return {
                    current_part: nested if not remaining_parts else {
                        'type': 'object',
                        'properties': nested
                    }
                }

        result = {}

        # Sort paths to ensure parent objects are processed before their children
        sorted_paths = sorted(self.schema_structure.items(), key=lambda x: len(x[0].split('.')))

        for path, info in sorted_paths:
            if not path:  # root level
                continue

            path_parts = path.split('.')
            current_dict = create_nested_dict(path_parts, info, path)

            for key, value in current_dict.items():
                if key not in result:
                    result[key] = value
                else:
                    result[key] = self._merge_schema_objects(result[key], value)

        return result

    def print_schema(self) -> None:
        """Print the clean schema as formatted JSON"""
        nested_schema = self._build_nested_schema()
        schema_json = json.dumps(nested_schema, indent=2)

        console = Console()
        syntax = Syntax(schema_json, "json", theme="monokai", line_numbers=True)
        console.print(syntax)

    def analyze_file(self, file_path: str) -> None:
        """Convenience method to analyze a JSON file directly."""
        data = self.load_json(file_path)
        self.analyze_json(data)

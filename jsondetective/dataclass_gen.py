from typing import Dict, Any



def generate_dataclass_code(schema: Dict[str, Any], class_name: str = "Root") -> str:
    """Generate Python code for dataclasses based on the JSON schema."""

    # Track all classes we need to generate
    classes = []

    def type_mapping(type_info: Dict[str, Any], field_name: str) -> str:
        """Map JSON schema types to Python types."""
        type_name = type_info.get('type', 'any')

        if type_name == 'array':
            item_type = 'Any'
            if 'items' in type_info:
                item_class_name = f"{class_name}{field_name.title()}"
                item_type = generate_nested_class(type_info['items'], item_class_name)
            return f"List[{item_type}]"
        elif type_name == 'object':
            nested_class_name = f"{class_name}{field_name.title()}"
            return generate_nested_class(type_info, nested_class_name)
        elif type_name == 'string':
            # Check examples for datetime strings
            examples = type_info.get('examples', [])
            if examples and any('GMT' in str(ex) for ex in examples):
                return 'datetime'
            return 'str'
        elif type_name == 'integer':
            return 'int'
        elif type_name == 'float':
            return 'float'
        elif type_name == 'boolean':
            return 'bool'
        elif type_name == 'null':
            return 'None'
        return 'Any'

    def generate_nested_class(schema_part: Dict[str, Any], nested_class_name: str) -> str:
        """Generate a nested dataclass for complex objects."""
        if 'properties' not in schema_part and schema_part.get('type') != 'object':
            return type_mapping(schema_part, '')

        properties = schema_part.get('properties', {})
        if not properties:
            return 'Dict[str, Any]'

        class_code = [f"@dataclass\nclass {nested_class_name}:"]

        for prop_name, prop_info in properties.items():
            is_optional = prop_info.get('optional', False)
            python_type = type_mapping(prop_info, prop_name)

            if is_optional:
                python_type = f"Optional[{python_type}]"
                default_value = " = None"
            else:
                default_value = ""

            # Convert snake_case to valid Python identifier
            valid_name = prop_name.replace('-', '_')

            # Add field with type annotation
            class_code.append(f"    {valid_name}: {python_type}{default_value}")

        classes.append('\n'.join(class_code))
        return nested_class_name

    # Generate the root class
    generate_nested_class({"type": "object", "properties": schema}, class_name)

    # Combine all classes with proper imports
    imports = [
        "from dataclasses import dataclass, field",
        "from typing import List, Optional, Dict, Any",
        "from datetime import datetime",
        ""
    ]

    return '\n\n'.join(imports + classes)


def schema_to_dataclass_file(schema: Dict[str, Any], output_file: str, class_name: str = "TinderData") -> None:
    """Generate a .py file containing the dataclass definitions."""
    code = generate_dataclass_code(schema, class_name)

    with open(output_file, 'w') as f:
        f.write(code)

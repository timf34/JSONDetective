import click
from rich.console import Console
from pathlib import Path
import json
from typing import Any, Optional

from .analyzer import JSONSchemaAnalyzer
from .dataclass_gen import schema_to_dataclass_file, generate_dataclass_code

console = Console()


def try_load_json(file_path: Path, encoding: str) -> Optional[Any]:
    """
    Attempt to load JSON file with specified encoding.
    Returns the parsed JSON data if successful, None if failed.
    """
    try:
        with file_path.open('r', encoding=encoding) as f:
            return json.load(f)
    except (UnicodeDecodeError, UnicodeError):
        return None
    except json.JSONDecodeError as e:
        # If it's a BOM error, return None to try next encoding
        if "BOM" in str(e):
            return None
        # For other JSON errors, we should raise them as they indicate malformed JSON
        raise


def load_json_with_fallback(file_path: Path) -> Any:
    """
    Try to load JSON file with multiple encodings.
    Raises click.ClickException if all attempts fail.
    """
    # List of encodings to try, in order of preference
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']

    for encoding in encodings:
        data = try_load_json(file_path, encoding)
        if data is not None:
            console.print(f"[dim]Successfully loaded JSON with {encoding} encoding[/dim]")
            return data

    # If we get here, none of the encodings worked
    raise click.ClickException(
        "Failed to load JSON file. Tried the following encodings: " +
        ", ".join(encodings)
    )


@click.command()
@click.argument(
    'json_path',
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--create-dataclass", "-d",
    is_flag=True,
    help="Generate Python dataclass code",
)
@click.option(
    "--output-path", "-o",
    type=click.Path(path_type=Path),
    help="Path to save the generated dataclass file (optional)",
)
@click.option(
    "--class-name", "-c",
    default="Root",
    help="Name of the root dataclass (default: Root)",
)
def main(json_path: Path, create_dataclass: bool, output_path: Path, class_name: str) -> None:
    """
    Analyze JSON files and optionally generate Python dataclasses.

    JSON_PATH: Path to the JSON file to analyze

    Examples:
        jsondetective data.json
        jsondetective data.json --create-dataclass
        jsondetective data.json -d -o my_classes.py
        jsondetective data.json -d -c MyDataClass
    """
    try:
        analyzer = JSONSchemaAnalyzer()

        # Use the new fallback loading function
        data = load_json_with_fallback(json_path)
        analyzer.analyze_json(data)

        console.print("\n[bold blue]JSON Schema:[/bold blue]")
        analyzer.print_schema()

        if create_dataclass:
            schema = analyzer._build_nested_schema()

            if output_path:
                schema_to_dataclass_file(schema, output_path, class_name)
                console.print(f"\n[bold green]Dataclass code saved to {output_path}[/bold green]")
            else:
                code = generate_dataclass_code(schema, class_name)
                console.print("\n[bold blue]Generated Dataclass Code:[/bold blue]")
                console.print(code)

    except click.ClickException:
        raise
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise click.Abort()


if __name__ == "__main__":
    main()

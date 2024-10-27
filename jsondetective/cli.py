import click
from rich.console import Console
from pathlib import Path

from .analyzer import JSONSchemaAnalyzer
from .dataclass_gen import schema_to_dataclass_file

console = Console()


@click.command()
@click.option(
    "--json-path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to the JSON file to analyze",
)
@click.option(
    "--create-dataclass",
    is_flag=True,
    help="Generate Python dataclass code",
)
@click.option(
    "--output-path",
    type=click.Path(path_type=Path),
    help="Path to save the generated dataclass file (optional)",
)
@click.option(
    "--class-name",
    default="Root",
    help="Name of the root dataclass (default: Root)",
)
def main(json_path: Path, create_dataclass: bool, output_path: Path, class_name: str) -> None:
    """
    Analyze JSON files and optionally generate Python dataclasses.
    """
    try:
        # Initialize analyzer
        analyzer = JSONSchemaAnalyzer()

        # Analyze the JSON file
        with json_path.open('r', encoding='utf-8') as f:
            data = analyzer.load_json(f)

        analyzer.analyze_json(data)

        # Print the schema
        console.print("\n[bold blue]JSON Schema:[/bold blue]")
        analyzer.print_schema()

        if create_dataclass:
            schema = analyzer._build_nested_schema()

            if output_path:
                # Save to file
                schema_to_dataclass_file(schema, output_path, class_name)
                console.print(f"\n[bold green]Dataclass code saved to {output_path}[/bold green]")
            else:
                # Print to console
                code = analyzer.generate_dataclass_code(schema, class_name)
                console.print("\n[bold blue]Generated Dataclass Code:[/bold blue]")
                console.print(code)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise click.Abort()


if __name__ == "__main__":
    main()

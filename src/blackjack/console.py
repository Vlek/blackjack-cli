"""
Entryway into the project for console-based usage.
"""

import rich_click as click


@click.command()
def main() -> None:
    """Entry into the project."""
    click.echo("Hello world")

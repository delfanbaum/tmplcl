import typer

from tmplcl.app import app
from tmplcl.commands import copy_template


def main():
    """
    Passthrough to run the app
    """
    app()

def copy():
    """
    Passthrough to run just the copy command for convenience
    """
    typer.run(copy_template)

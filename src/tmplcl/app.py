import typer

from tmplcl.commands import (
    add_template,
    copy_template,
    delete_template,
    list_templates,
    show_template,
    update_template,
)
from tmplcl.model import DB

app = typer.Typer()
db = DB()


@app.command()
def copy(template: str):
    """Copies the requested template to your clipboard"""
    copy_template(template, db)


@app.command()
def delete(template: str):
    """Deletes the template with the provided identifier"""
    delete_template(template, db)


@app.command()
def add(template_name: str, template_string: str):
    """Adds a template with the provided identifier and string"""
    add_template(template_name, template_string, db)


@app.command()
def list():
    """
    Lists all available templates, including a preview of each
    """
    list_templates(db)


@app.command()
def show(template_name: str):
    """
    Displays the full text of a given template
    """
    show_template(template_name, db)


@app.command()
def update(template_name: str, template_string: str):
    """Updates a given template with a new string"""
    update_template(template_name, template_string, db)

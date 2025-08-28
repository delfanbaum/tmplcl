import pyperclip
from rich import print

from tmplcl.model import DB, Template


# CREATE
def add_template(identifier: str, template_str: str) -> None:
    """
    Adds a new template to the database
    """
    db = DB()
    db.insert(Template(identifier=identifier, template=template_str))


# READ
def copy_template(identifier: str) -> None:
    """
    Finds a template by its id and copies the resultant string to the clipboard
    """
    db = DB()
    template, _ = db.get(identifier)
    pyperclip.copy(template.template)


def list_templates() -> None:
    """
    Lists all available templates, with a truncated preview of template string
    """
    db = DB()
    for template in db.get_all():
        id, templ = template.display()
        print(f"{id}: [italic]{templ:t100}[/italic]...")


def show_template(identifer: str) -> None:
    """
    Shows the full "template" for a given identifier, formatted to highlight any
    internal template string options
    """
    db = DB()
    template, _ = db.get(identifer)
    print(f"{template.display()[1]}")


# UPDATE
def update_template(identifier: str, template_str) -> None:
    """
    Updates a given template id with a new template string
    """
    db = DB()
    db.update(identifier, template_str)


# DESTROY
def delete_template(identifier: str) -> None:
    """
    Finds a template by its id and deletes it from the database
    """
    db = DB()
    db.delete(identifier)

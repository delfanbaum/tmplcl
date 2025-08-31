import pyperclip
from rich import print

from tmplcl.model import DB, Template


# CREATE
def add_template(identifier: str, template_str: str, db: DB) -> None:
    """
    Adds a new template to the database
    """
    db.insert(Template(identifier=identifier, template=template_str))


# READ
def copy_template(identifier: str, db: DB) -> None:
    """
    Finds a template by its id and copies the resultant string to the clipboard
    """
    template, _ = db.get(identifier)
    pyperclip.copy(template.template)


def list_templates(db: DB) -> None:
    """
    Lists all available templates, with a truncated preview of template string
    """
    truncate = 100  # maybe this becomes configurable someday
    for template in db.get_all():
        id, templ = template.display()
        if len(templ) > truncate:
            print(f"{id}: [italic]{templ:.truncate}[/italic]...")
        else:
            print(f"{id}: [italic]{templ}[/italic]")


def show_template(identifer: str, db: DB) -> None:
    """
    Shows the full "template" for a given identifier, formatted to highlight any
    internal template string options
    """
    template, _ = db.get(identifer)
    print(f"{template.display()[1]}")


# UPDATE
def update_template(identifier: str, template_str: str, db: DB) -> None:
    """
    Updates a given template id with a new template string
    """
    db.update(identifier, template_str)


# DESTROY
def delete_template(identifier: str, db: DB) -> None:
    """
    Finds a template by its id and deletes it from the database
    """
    db.delete(identifier)

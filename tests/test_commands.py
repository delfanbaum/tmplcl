import pyperclip

from tmplcl.commands import (
    add_template,
    copy_template,
    delete_template,
    list_templates,
    update_template,
)


class TestCommands:
    """
    Command API tests; note that error handling is tested on the model tests. 
    """

    def test_add_template(self, test_db):
        """
        Ensures that we can add a template to the db given an identifier and
        template string
        """

        add_template("baz", "biff", db=test_db)

        # since we include one template in the DB as a part of the test setup
        assert len(test_db.get_all()) == 2

    def test_copy_template(self, test_db):
        """
        Ensures that copy_template copies the "foo" pre-baked template to the
        clipboard
        """
        copy_template("foo", test_db)
        assert pyperclip.paste() == "bar"

    def test_list_templates(self, test_db, capsys):
        """
        Ensures that we can list our templates
        """
        list_templates(test_db)

        assert "foo: bar" in capsys.readouterr().out

    def test_update_template(self, test_db):
        """
        Ensures we can update a template (starts as "bar" in the DB)
        """
        update_template("foo", "baz", test_db)

        assert test_db.get("foo")[0].template == "baz"

    def test_delete_template(self, test_db):
        """
        Ensures we can delete a template
        """
        delete_template("foo", test_db)
        assert not test_db.get_all()

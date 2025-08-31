import pytest
from tinydb import TinyDB

from tmplcl.models import (
    DB,
    CorruptedTemplate,
    DuplicateTemplateId,
    Template,
    TemplateNotFound,
)


class TestTemplate:
    """
    Template tests
    """

    def test_display(self):
        """
        Tests our display function
        """

        template = Template(identifier="foo", template="bar")
        identifier, template_str = template.display()
        assert identifier == "[bold blue]foo[/bold blue]"
        assert template_str == "bar"

    def test_display_with_placeholders(self):
        """
        Tests our display function
        """

        template = Template(identifier="foo", template="bar {}")
        identifier, template_str = template.display()
        assert identifier == "[bold blue]foo[/bold blue]"
        assert template_str == r"bar [magenta]{}[/magenta]"


class TestDB:
    """
    Database tests, mostly around error handling
    """

    def test_field_access(self, tmp_path):
        """
        Smoke test for initialization and access
        """
        # make sure there are no collisions with our fixture
        data_dir = tmp_path / "testing"
        data_dir.mkdir()

        db = DB(data_dir=data_dir)

        assert isinstance(db.db, TinyDB)
        assert db.data_dir == data_dir
        assert (data_dir / "data.json").is_file()

    def test_raises_duplate_id(self, test_db, test_tmpl):
        """
        Since test_tmpl is already in the db, it should error; actual insertion
        is tests in test_commands
        """
        with pytest.raises(DuplicateTemplateId):
            test_db.insert(test_tmpl)

    def test_not_found(self, test_db):
        """
        Assure that we raise an error if we can't find a given template
        """
        with pytest.raises(TemplateNotFound):
            test_db.get("baz")

    def test_validation_error(self, test_db):
        """
        Assures that if the user monkeyed with the db and made it invalid, we
        raise an error
        """

        # insert invalid data into DB directly
        test_db.db.insert({"identifier": "baz", "template": ""})

        with pytest.raises(CorruptedTemplate):
            test_db.get("baz")

import pytest

from tmplcl.models import DB, Template


@pytest.fixture()
def test_tmpl() -> Template:
    """
    Test template instance
    """
    return Template(identifier="foo", template="bar")


@pytest.fixture()
def test_db(tmp_path, test_tmpl) -> DB:
    """
    Test DB instance with a single template entry
    """
    db = DB(data_dir=tmp_path)

    db.insert(test_tmpl)

    return db

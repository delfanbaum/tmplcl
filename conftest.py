import pytest

from tmplcl.model import DB, Template


@pytest.fixture()
def test_db(tmp_path) -> DB:
    """
    Test DB instance with a single template entry
    """
    db = DB(data_dir=tmp_path)

    sample = Template(identifier="foo", template="bar")
    db.insert(sample)

    return db

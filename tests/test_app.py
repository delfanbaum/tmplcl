import pytest
from typer.testing import CliRunner

from tmplcl import app
from tmplcl.commands import add_template
from tmplcl.models import DB, Template

runner = CliRunner()


class TestApp:
    def test_app_commands(self):
        """Ensures all the expected commands are listed in the help output"""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "copy" in result.output
        assert "delete" in result.output
        assert "add" in result.output
        assert "show" in result.output
        assert "update" in result.output
        assert "list" in result.output

    @pytest.mark.parametrize("command", ["copy", "update", "show"])
    def test_not_found(self, command, monkeypatch, test_db):
        """
        Ensures that copy_template, when getting a missing template, returns
        that error
        """
        monkeypatch.setattr(DB, "get", test_db.get)
        monkeypatch.setattr(DB, "update", test_db.update)
        runner_args = [command, "not_found"]
        if command in ["update"]:
            runner_args.append("foo")

        result = runner.invoke(app, runner_args)
        assert result.exit_code == 1
        assert "Unable to find the requested template" in result.output

    @pytest.mark.parametrize("command", ["copy", "show"])
    def test_corrupted(self, command, monkeypatch, test_db):
        """
        Ensures that copy_template, when getting a corrupted template, returns
        that error
        """
        test_db.db.insert({"identifier": "baz", "template": ""})
        monkeypatch.setattr(DB, "get", test_db.get)
        runner_args = [command, "baz"]
        result = runner.invoke(app, runner_args)
        assert result.exit_code == 1
        assert "appears to have been corrupted" in result.output

    def test_list(self, monkeypatch, test_db):
        """
        Successfully lists templates
        """
        monkeypatch.setattr(DB, "get_all", test_db.get_all)
        runner_args = ["list"]

        result = runner.invoke(app, runner_args)
        assert result.exit_code == 0
        assert "foo: bar" in result.output

    def test_list_truncate(self, monkeypatch, test_db):
        """
        Successfully lists templates
        """
        long_string = "a" * 100
        add_template("baz", long_string, test_db)
        monkeypatch.setattr(DB, "get_all", test_db.get_all)
        runner_args = ["list", "--show-chars", "10"]

        result = runner.invoke(app, runner_args)
        assert result.exit_code == 0
        assert f"baz: {'a' * 10}...\n" in result.output

    def test_delete(self, monkeypatch, test_db):
        """
        Successfully delete a given template
        """
        monkeypatch.setattr(DB, "delete", test_db.delete)
        runner_args = ["delete", "foo"]

        result = runner.invoke(app, runner_args)
        assert result.exit_code == 0

        assert not test_db.get_all()

    def test_delete_does_not_err_on_missing(self, monkeypatch, test_db):
        """
        If a template doesn't exist, we don't care, so fail silently
        """
        monkeypatch.setattr(DB, "delete", test_db.delete)
        runner_args = ["delete", "bar"]

        result = runner.invoke(app, runner_args)
        assert result.exit_code == 0

        # ensure we didn't actually change the database
        assert len(test_db.get_all()) == 1

    def test_add(self, monkeypatch, test_db):
        """
        Tests that we can successfully add to the db via the CLI
        """
        monkeypatch.setattr(DB, "insert", test_db.insert)
        runner_args = ["add", "bar", "baz"]

        result = runner.invoke(app, runner_args)
        assert result.exit_code == 0
        assert len(test_db.get_all()) == 2

    def test_update_validation_error(self, monkeypatch, test_db):
        """
        If we try to update a template with an invalid template string, we tell
        the user this
        """
        monkeypatch.setattr(DB, "update", test_db.update)
        runner_args = ["update", "foo", ""]
        result = runner.invoke(app, runner_args)
        assert result.exit_code == 1
        assert "Invalid replacement template string" in result.output
        assert test_db.get("foo")[0].template == "bar"

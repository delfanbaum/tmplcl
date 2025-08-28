# Template to Clipboard

Templates to your clipboard: because sometimes you *just* can't be bothered to
type it again. While this utility was created as an exercise to relearn `typer`
(which is great, though really all CLI tools should be "rewritten in Rust") and
a few other tools, but hopefully it's at least of some use to some folks.
Eventually, the idea is to also leverage [template
strings](https://peps.python.org/pep-0750/) once those become available, because
really that is a great idea.

## Installation

The recommended installation path is via the `uv tool` interface, installing via
(for now, until it's stable enough to put on `pypi`):

```sh
uv tool install  git+https://github.com/delfanbaum/tmplcl
```

## Usage

This package provides two executable commands: `tmplcl` and `tcl`. `tmplcl` is
the "app" version of the tool, allowing you to perform all the expected CRUD
tasks such as creating, listing, deleting, and updating your various templates.
`tcl` is essentially just a shortcut for `tmplcl copy TEMPLATE_ID`, because who
wants to do all that typing.

The usage for each is as follows:

```console
uv run tmplcl --help
```

```console
uv run tcl --help
```

## Data Storage

Following the [XDG Base Directory
Specification](https://specifications.freedesktop.org/basedir-spec/latest/),
data will stored in `$XDG_DATA_HOME/tmplcl`. 

If you would like to define your templates manually, it's all just JSON, so open
up `$XDG_DATA_HOME/tmplcl/templates.json` and have at it. The schema is roughly
as follows:

(TBD)

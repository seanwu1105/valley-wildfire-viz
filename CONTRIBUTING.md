# How to Contribute

See [instruction](instructions.pdf) for specifications.

## Getting Started

> It is recommended to use [asdf](https://asdf-vm.com/) to manage the versions
> of the used languages, including Python and Node.js. See
> [.tool-versions](.tool-versions) for the versions used in this project.

Install Python 3.10 or later.

Install Poetry 1.3.2 or later. See
[Poetry's documentation](https://python-poetry.org/docs/) for details.

Install the project's dependencies:

```sh
poetry install --no-root
```

Since the pre-commit hooks require Node.js, you need to install it. See
[documentation](https://nodejs.org/en/download/) for details.

Install pre-commit hooks:

```sh
poetry run pre-commit install
```

Activate the virtual environment:

```sh
poetry shell
```

## Running Tests

```sh
poetry run pytest
```

## Caveats

If you found `Could not load the qt platform plugin "xcb" in "" even though it`
error, see
[this](https://askubuntu.com/questions/1271976/could-not-load-the-qt-platform-plugin-xcb-in-even-though-it-was-found)
for details.

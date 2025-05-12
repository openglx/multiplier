# multiplier

A simple web app to help children train for their
[Multiplication Tables Check](https://www.gov.uk/government/collections/multiplication-tables-check).

## Installing and running

This application uses `poetry` to manage dependencies.

Install [poetry](https://python-poetry.org/docs/):

```shell
pipx install poetry
```

Clone this repository.

"Install" this application:

```shell
poetry install
```

Run with:

```shell
poetry run gunicorn -w 1 'multiplier:create_app()'
```

If developing, use the Flask debug with:

```shell
poetry run flask --app multiplier --debug run
```

There are no other requisites, this doesn't use database
or any configuration.

It doesn't even need cookies!

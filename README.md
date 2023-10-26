# Cloud Storage

Simple local cloud storage application.

## Stack

Following technologies are being used:

-   Flask
-   Flask-Sessions
-   SQLite3

## Install application

To install the application, run following command

```sh
$ pip install -e .
```

## Run application

Enter following command for deplying the application

```sh
$ flask --app cloud_storage run
```

or add `debug` flag, i.e.,

```sh
$ flask --app cloud_storage run --debug
```

## Running tests

To initialize the tests, simply run

```sh
$ pytest
```

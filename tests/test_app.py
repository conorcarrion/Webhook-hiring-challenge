from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.testing import TestCase
from testing.postgresql import Postgresql
from conftest import data as test_data
import source.app
import pytest


@pytest.fixture()
def app():
    app = source.app.create_app()
    app.config.update({
        "TESTING": True,
    })
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # other setup can go here
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


def test_request_example(client):
    response = client.get("/")
    assert b"Welcome to my Github Webhook Handler" in response.data



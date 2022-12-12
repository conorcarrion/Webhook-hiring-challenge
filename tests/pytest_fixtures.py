import pytest
from source.app import app
from flask_sqlalchemy import SQLAlchemy
from config.config import TestingConfig


@pytest.fixture
def client():

    app.config["TESTING"] = True
    client = app.test_client()

    yield client


@pytest.fixture
def db(app):
    app.config.from_object(TestingConfig())
    db = SQLAlchemy(app)

    # Create all the tables in the database
    db.create_all()

    yield db

    # Drop all the tables in the database
    db.drop_all()


@pytest.fixture
def valid_payload_headers():
    return {"content-type": "application/json", "X-Github-Event": "push"}


@pytest.fixture
def valid_payload_body():
    return {
        "ref": "refs/heads/main",
        "after": "123456789abcdef",
        "repository": {"name": "test_repo", "default_branch": "main"},
        "head_commit": {
            "timestamp": "2022-12-11T12:34:56Z",
            "author": {
                "name": "Wednesday Addams",
                "email": "Wednesdayaddams@example.com",
                "username": "WednesdayAddams",
            },
            "message": "Add new feature",
        },
    }


@pytest.fixture
def valid_change_event_data():
    return {
        "ts": "2022-12-11T12:34:56Z",
        "source": "github",
        "change_type": "push",
        "data": {
            "repository": "test_repo",
            "branch": "main",
            "commit": "123456789abcdef",
            "author": {
                "name": "Wednesday Addams",
                "email": "Wednesdayaddams@example.com",
                "username": "WednesdayAddams",
            },
            "message": "Add new feature",
        },
    }


@pytest.fixture
def invalid_payload_headers():
    return {"content-type": "application/json", "X-Github-Event": "issues"}


@pytest.fixture
def invalid_payload_body():
    return {
        "ref": "refs/heads/devbranch",
        "after": "123456789abcdef",
        "repository": {"name": "test_repo", "default_branch": "main"},
        "head_commit": {
            "timestamp": "2022-12-11T12:34:56Z",
            "author": {
                "name": "Wednesday Addams",
                "email": "Wednesdayaddams@example.com",
                "username": "WednesdayAddams",
            },
            "message": "Add new feature",
        },
    }

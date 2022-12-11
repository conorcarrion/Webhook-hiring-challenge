import json
import pytest
from source.app import flask_app, db, ChangeEvent


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    client = flask_app.test_client()

    yield client


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200, "Get request from homepage was not succesful"
    assert (
        response.data == "Welcome to my Github Webhook Handler"
    ), "Get request homepage message not showing"


def test_webhook_receiver_push_event(client):
    # Set up a test payload that simulates a push event to the default branch
    payload = {
        "headers": {"content-type": "application/json", "X-Github-Event": "push"},
        "json": {
            "default_branch": "main",
            "ref": "refs/heads/main",
            "after": "123456789abcdef",
            "repository": {"name": "test_repo"},
            "head_commit": {
                "author": {
                    "name": "Wednesday Addams",
                    "email": "Wednesdayaddams@example.com",
                },
                "timestamp": "2022-12-11T12:34:56Z",
                "message": "Add new feature",
            },
        },
    }

    # Make a POST request with the test payload
    response = client.post("/github", data=payload, content_type="application/json")
    assert response.status_code == 200, "post request to /github not succesful"
    assert (
        response.data == "Webhook received and information added to database"
    ), "post request to /github message not shown"

    # Check that the correct information was added to the database
    change_event = ChangeEvent.query.first()
    assert change_event.data == {
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
            },
            "message": "Add new feature",
        },
    }, "Post request to /github, Database entry does not match the payload"


def test_webhook_receiver_non_push_event(client):
    # Set up a test payload that simulates a non-push event
    payload = {
        "headers": {"content-type": "application/json", "X-Github-Event": "pull"},
        "json": {
            "default_branch": "main",
            "ref": "refs/heads/main",
            "after": "123456789abcdef",
            "repository": {"name": "my_repo"},
            "head_commit": {
                "author": {"name": "John Doe", "email": "johndoe@example.com"},
                "timestamp": "2022-12-11T12:34:56Z",
                "message": "Add new feature",
            },
        },
    }
    response = client.post("/github", data=payload, content_type="application/json")
    assert (
        response.status_code == 200
    ), "post request to /github with non-push event not succesful"
    assert (
        response.data == "Push request not for default branch, not actioned"
    ), "post request to /github with non-push event not showing correct message"

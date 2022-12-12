import json
import pytest
from source.app import ChangeEvent, app
from pytest_fixtures import (
    db,
    client,
    valid_payload_headers,
    valid_payload_body,
    valid_change_event_data,
    invalid_payload_headers,
    invalid_payload_body,
)

# Test get request to homepage gives correct status code and welcome message
def test_homepage(client):
    test_response = client.get("/")
    assert test_response.status_code == 200

    # Verify that the test_response message is "Welcome to my Github Webhook Handler"
    assert b"Welcome to my Github Webhook Handler" in test_response.data


# positive/functional test for a push event to the main branch
def test_webhook_receiver_push_event(client, valid_payload_headers, valid_payload_body):

    # Simulate a POST request with the valid test fixtures
    test_response = client.post(
        "/github", headers=valid_payload_headers, json=valid_payload_body
    )

    # Check that the app response was correct
    assert test_response.status_code == 200
    assert b"Webhook received and information added to database" in test_response.data


def test_change_event(valid_change_event_data):
    # Check that the correct information was added to the database
    change_event = ChangeEvent(valid_change_event_data)
    query = db.session.query(ChangeEvent).first()
    assert change_event.id == query.id
    assert change_event.data == valid_change_event_data
    assert query.data == valid_change_event_data


def test_webhook_receiver_non_push_event(
    client, invalid_payload_headers, valid_payload_body
):
    # Simulate a POST request with a non-push Github Event in the headers
    # using pytest fixture "invalid_payload_headers"

    test_response = client.post(
        "/github", headers=invalid_payload_headers, json=valid_payload_body
    )
    # Check that the app response was correct
    assert test_response.status_code == 200
    assert b"Request is not a push request, not actioned" in test_response.data


def test_webhook_receiver_non_mainbranch_event(
    client, valid_payload_headers, invalid_payload_body
):
    # Simulate a POST request with a push to a non-main branch.

    test_response = client.post(
        "/github", headers=valid_payload_headers, json=invalid_payload_body
    )
    # Check that the app response was correct
    assert test_response.status_code == 200
    assert b"Push request not for default branch, not actioned" in test_response.data

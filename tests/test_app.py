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
    assert test_response.data == b"Welcome to my Github Webhook Handler"


# positive/functional test for a push event to the main branch
def test_webhook_receiver_push_event(
    client, valid_payload_headers, valid_payload_body, valid_change_event_data
):

    # Simulate a POST request with the valid test fixtures
    test_response = client.post(
        "/github", headers=valid_payload_headers, json=valid_payload_body
    )
    test_json = test_response.json

    # Check that the correct information was added to the database
    with app.app_context():
        test_change_event = ChangeEvent(test_json)
        change_event_query = ChangeEvent.query.order_by(ChangeEvent.id.desc()).first()
        assert change_event_query.data == valid_change_event_data.replace("'", '"')

    # Check that the app response was correct
    assert test_response.status_code == 200
    assert b"Webhook received and information added to database" in test_response.data


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

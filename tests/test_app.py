import json
import pytest
from source.app import flask_app, db, ChangeEvent
from pytest_fixtures import (
    client,
    valid_payload_headers,
    valid_payload_body,
    valid_change_event_data,
    invalid_payload_headers,
    invalid_payload_body,
)


def test_homepage(client):
    test_response = client.get("/")
    assert test_response.status_code == 200

    # Verify that the test_response message is "Welcome to my Github Webhook Handler"
    assert test_response.data == b"Welcome to my Github Webhook Handler"


def test_webhook_receiver_push_event(
    client, valid_payload_headers, valid_payload_body, valid_change_event_data
):

    # Make a POST request with the test payload
    test_response = client.post(
        "/github", headers=valid_payload_headers, json=valid_payload_body
    )
    test_json = test_response.json

    # Check that the correct information was added to the database
    with flask_app.app_context():
        test_change_event = ChangeEvent(test_json)
        change_event_query = ChangeEvent.query.order_by(ChangeEvent.id.desc()).first()
        assert change_event_query.data == valid_change_event_data

    assert test_response.status_code == 200
    assert b"Webhook received and information added to database" in test_response.data


def test_webhook_receiver_non_push_event(
    client, invalid_payload_headers, valid_payload_body
):
    # Set up a test payload that simulates a non-push event

    test_response = client.post(
        "/github", headers=invalid_payload_headers, json=valid_payload_body
    )

    assert test_response.status_code == 200
    assert b"Request is not a push request, not actioned" in test_response.data


def test_webhook_receiver_non_mainbranch_event(
    client, valid_payload_headers, invalid_payload_body
):
    # Set up a test payload that simulates a non-push event

    test_response = client.post(
        "/github", headers=valid_payload_headers, json=invalid_payload_body
    )
    assert test_response.status_code == 200
    assert b"Push request not for default branch, not actioned" in test_response.data

from source.app import create_app
from flask_sqlalchemy import SQLAlchemy
from flask.ext.testing import TestCase
from testing.postgresql import Postgresql
from conftest import data as test_data
import source.app
import pytest
import requests_mock
import json

# pytest fixtures

def test_create_app():
    DATABASE_TYPE='postgresql'
    DBAPI='psycopg2'
    HOST='testing'
    USER='testing'
    PASSWORD='testing'
    DATABASE='testing'
    PORT='5432'
    app = create_app(DATABASE_TYPE, DBAPI, USER, PASSWORD, HOST, PORT, DATABASE)
    assert app.config["SQLALCHEMY_DATABASE_URI"] == 'postgresql+psycopg2://testing:testing@testing:5432/testing'
    return app

  
@pytest.fixture
def json_request():
    with open('webhook_example.json') as outfile:
        json = json.load(outfile)
    
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'http://test.com', json=json)
        print(requests.get('http://test.com').text)


# flask() 

# sqlalchemy()

# Event()


# Homepage get req
def test_example(client):
 response = client.get("/")
 assert response.status_code == 200
 assert "Welcome to my Github Webhook Handler" in response.data

# webhook to /github

# common issues are resolved properly
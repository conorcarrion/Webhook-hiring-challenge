from source.app import create_app, ChangeEvent
from flask.ext.testing import TestCase
from flask_sqlalchemy import SQLAlchemy

class TestBlog:
    def setup_class(self):
        db = SQLAlchemy()
        db.create_all()
        
        self.valid_change_event = ChangeEvent(
            id=1,
            data={'key1': 'value1', 'key2': 'value2'}
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

# test Flask(__name__) in create_app works
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

# test that GithubChangeEvent(event) converts an event with data x to:
def test_ChangeEvent():
    change_event_test_data = {'key1': 'value1', 'key2': 'value2'}
    created_change_event_object = ChangeEvent(change_event_test_data)
    assert created_change_event_object.id == 1
    assert created_change_event_object.data == {'key1': 'value1', 'key2': 'value2'}


# Homepage get req
def test_example(client):
 response = client.get("/")
 assert response.status_code == 200
 assert "Welcome to my Github Webhook Handler" in response.data

# webhook to /github returns data as 

# common issues are resolved properly
from flask import Flask
from source.app import create_flask_app, ChangeEvent, add_change_event_to_db
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy

#Test Class
class TestUnit(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
        
    # set up all required resources before testing
    def setup_class(self):
        self.db = SQLAlchemy()
        self.db.create_all()
        self.testdata = {'key1': 'value1', 'key2': 'value2'}
        self.valid_change_event = ChangeEvent(
            data=self.testdata
        )
    # destroy all items created during testing
    def teardown_class(self):
        self.db.session.rollback()
        self.db.session.close()

    # test if ChangeEvent class correctly creates database object
    def test_ChangeEvent(self):
        test_change_event_object = ChangeEvent(
            {'key1': 'value1', 'key2': 'value2'}
            )
        assert test_change_event_object == self.valid_change_event
        
    # test create_app correctly creates flask app and 
    def test_create_flask_app():
        DATABASE_TYPE='postgresql'
        DBAPI='psycopg2'
        HOST='testing'
        USER='testing'
        PASSWORD='testing'
        DATABASE='testing'
        PORT='5432'
        flask_app = create_flask_app(DATABASE_TYPE, DBAPI, USER, PASSWORD, HOST, PORT, DATABASE)
        assert flask_app.config[
            "SQLALCHEMY_DATABASE_URI"
            ] == 'postgresql+psycopg2://testing:testing@testing:5432/testing'

    # confirm add_change_event_to_db adds the ChangeEvent object to the database
    def test_add_change_event_to_db(self):
        add_change_event_to_db(self.db, self.valid_change_event)
        valid_event_added = self.db.Query(ChangeEvent).filter_by(data=self.testdata).first()
        assert isinstance(valid_event_added.id, int)
        assert valid_event_added.data == {'key1': 'value1', 'key2': 'value2'}

# testing / and /github
class TestViews(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_example(client):
        response = client.get("/")
        assert response.status_code == 200
        assert "Welcome to my Github Webhook Handler" in response.data

    def test_some_json(self, client):
        response = client.get("/github")
        self.assertEquals(response.json, dict(success=True))

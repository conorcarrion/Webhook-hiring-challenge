from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.testing import TestCase
from testing.postgresql import Postgresql
from conftest import data
from source.webhookhandler import webhook, Event


class MyTest(TestCase):
    
    SQLALCHEMY_DATABASE_URI = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    TESTING = True
    with Postgresql() as postgresql:
    app.config['SQLALCHEMY_DATABASE_URI'] = postgresql.url()

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        
        return create_app(self)


    def create_db(self):
        db = SQLAlchemy(app)
        return create_db(self)

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()


class test_new_event(MyTest):

    def test_(self):

        event = Event(data)
        db.session.add(event)
        db.session.commit()

        assert event in db.session

        


class TestViews(TestCase):
    def test_some_json(self):
        response = self.client.get("/github")
        self.assertEquals(response.json, dict(success=True))
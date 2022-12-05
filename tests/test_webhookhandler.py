from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.testing import TestCase

class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        db = SQLAlchemy(app)
        return app, db

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()


class SomeTest(MyTest):

    def test_something(self):

        event = Event()
        db.session.add(user)
        db.session.commit()

        # this works
        assert user in db.session

        response = self.client.get("/")

        # this raises an AssertionError
        assert user in db.session


class TestViews(TestCase):
    def test_some_json(self):
        response = self.client.get("/github")
        self.assertEquals(response.json, dict(success=True))
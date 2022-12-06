## My Python Micro-service for github push
# imports

import os
import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


# loading environment variables from .env file
load_dotenv()
DATABASE_TYPE = os.getenv("DATABASE_TYPE")
DBAPI = os.getenv("DBAPI")
HOST = os.getenv("HOST")
USER = os.getenv("USER1")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")

# instantiating Flask and configuring sqlalchemy database uri based on env variables
def create_flask_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config[
                "SQLALCHEMY_DATABASE_URI"
    ] = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    return app

flask_app = create_flask_app()

# instantiating sqlalchemy database
db = SQLAlchemy(flask_app)


# Database object to allow insertion of webhook information into sql database
class ChangeEvent(db.Model):

    __tablename__ = "changes"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)

    def __init__(self, data):
        self.data = data



# Converting event to database object and adding/committing to database.
def add_change_event_to_db(db, mod_request_json):

    change_event_object = ChangeEvent(mod_request_json)
    db.session.add(change_event_object)
    db.session.commit()


# Defining homepage behaviour
@flask_app.route("/")
def root():
    return "Welcome to my Github Webhook Handler"


# Filtering change events to only json, only main, only branch
def change_event_filter(request):
    confirm_json = request.headers["content-type"] == "application/json"
    confirm_push = request.headers["X-Github-Event"] == "push"
    confirm_main = request.json["ref"] == "refs/heads/main"
    return confirm_json and confirm_push and confirm_main


# Defining actions to take upon receiving a POST request to url/github
@flask_app.route("/github", methods=["POST"])
def webhook_receiver():
    # Request meets specification and is actioned
    if change_event_filter(request):
        change_event_body = request.json

        # information converted to format required
        mod_request_dict = {
            "ts": change_event_body["created"],
            "source": "github",
            "change_type": "push",
            "data": {
                "repository": change_event_body["repository"],
                "branch": change_event_body["ref"],
                "commit": change_event_body["after"],
                "author": change_event_body["pusher"],
                "message": change_event_body["head_commit"]["message"],
            },
        }
        mod_request_json = json.dumps(mod_request_dict)
        add_change_event_to_db(db, mod_request_json)
        return "Webhook received and information added to database", 200

    # Pushes to repository not on main branch are not actioned
    if not request.json["ref"] == "refs/heads/main":
        return "Success, non main branch push received but not added", 200

    # POST requests not json or push are flagged as bad requests.
    return 'Bad Request, ', 400


# create table as per ChangeEvent or ignore
db.create_all()


if __name__ == "__main__":
    flask_app.run(debug=True)

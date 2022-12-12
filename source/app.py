## My Python Micro-service for github push
# imports

import os
import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config.config import DevelopmentConfig


# instantiating Flask
def create_app():

    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig())
    return app


app = create_app()

# instantiating sqlalchemy database
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


class ChangeEvent(db.Model):
    __tablename__ = "changes"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return "<Change Event Data = {}>".format(self.data)


# TODO @classmethod
# class ChangeEventRepository:
#     def create():

#     def read():

#     def update():

#     def delete():


# Defining homepage behaviour
@app.route("/")
def root():
    return "Welcome to my Github Webhook Handler"


# Defining actions to take upon receiving a POST request to url/github
@app.route("/github", methods=["POST"])
def webhook_receiver():

    # Filtering change events to only json, only main, only branch
    def change_event_filter(request):
        # confirm request format is json
        confirm_json = request.headers["content-type"] == "application/json"
        # confirm webhook trigger is due to a push
        confirm_push = request.headers["X-Github-Event"] == "push"
        # identify the default branch of the repository
        default_branch = request.json["repository"]["default_branch"]
        # confirm the push is for the default branch
        confirm_default = request.json["ref"].split("/")[-1] == default_branch
        return confirm_json and confirm_push and confirm_default

    # Request meets specification and is actioned
    if change_event_filter(request):
        request_body = request.json

        # information converted to format required
        change_event_data = json.dumps(
            {
                # time of the push event
                "ts": request_body["head_commit"]["timestamp"],
                "source": "github",
                "change_type": "push",
                "data": {
                    # repo name
                    "repository": request_body["repository"]["name"],
                    # name of the branch changes were pushed to
                    "branch": request_body["ref"].split("/")[-1],
                    # commit sha that is the HEAD after the push
                    "commit": request_body["after"],
                    # name/email of the author
                    "author": request_body["head_commit"]["author"],
                    # last commit message that is not a merge commit
                    "message": request_body["head_commit"]["message"],
                },
            }
        )

        db.session.add(ChangeEvent(change_event_data))
        db.session.commit()
        return "Webhook received and information added to database", 200

    # Pushes to repository not on main branch are not actioned
    if (
        not request.json["ref"].split("/")[-1]
        == request.json["repository"]["default_branch"]
    ):
        return "Push request not for default branch, not actioned", 200
    # Non push post requests are not actioned
    if not request.headers["X-Github-Event"] == "push":
        return "Request is not a push request, not actioned", 200

    # POST requests not json or push are flagged as bad requests.
    return "Bad Request, ", 400


# run code
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

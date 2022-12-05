import os
import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
DATABASE_TYPE = os.getenv("DATABASE_TYPE")
DBAPI = os.getenv("DBAPI")
HOST = os.getenv("HOST")
USER = os.getenv("USER1")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

db = SQLAlchemy(app)


class Event(db.Model):
    '''Event parameters'''
    __tablename__ = "changes"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)

    def __init__(self, data):
        self.data = data


@app.route("/")
def root():
    return "Welcome to My Github Webhook Handler"


@app.route("/github", methods=["POST"])
def webhook():

    confirm_json = request.headers["content-type"] == "application/json"
    confirm_push = request.headers["X-Github-Event"] == "push"
    confirm_main = request.json["ref"] == "refs/heads/main"
    if confirm_json and confirm_push and confirm_main:
        event = request.json
        data = {
            "ts": event["created"],
            "source": "github",
            "change_type": "push",
            "data": {
                "repository": event["repository"],
                "branch": event["ref"],
                "commit": event["after"],
                "author": event["pusher"],
                "message": event["head_commit"]["message"],
            },
        }
        data_json = json.dumps(data, indent=4)
        event = Event(data_json)
        db.session.add(event)
        db.session.commit()
        return "200 Event Data added to Database"

    elif not confirm_json:
        return '415	Unsupported Media Type. The request data format is not supported by the server. Only Json is accepted'

    elif not confirm_push:
        return '202 Only push events accepted to Database'

    elif not confirm_main:
        return '202 Only main branch events accepted to Database'

    else:
        return '400 Bad Request'


db.create_all()


if __name__ == "__main__":
    app.run(debug=True)

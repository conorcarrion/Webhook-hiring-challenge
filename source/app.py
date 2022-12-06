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


def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    print(app.config["SQLALCHEMY_DATABASE_URI"])
    return app 


app = create_app()
db = SQLAlchemy(app)


class Event(db.Model):
    '''Event parameters'''
    __tablename__ = "changes"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)

    def __init__(self, data):
        self.data = data

def upserter(data):
    data_json = json.dumps(data)
    event = Event(data_json)
    db.session.add(event)
    db.session.commit()

    
@app.route("/")
def root():
    return "Welcome to my Github Webhook Handler"


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
        
        upserter(data)

        return f"Webhook received: \n\n {data}", 200

    elif not confirm_json:
        return 'Unsupported Media Type. The request data format is not supported by the server. Only Json is accepted', 415	

    elif not confirm_push:
        return 'Only push events accepted to Database', 202

    elif not confirm_main:
        return 'Only main branch events accepted to Database', 202 

    else:
        return 'Bad Request', 400 
db.create_all()


if __name__ == "__main__":
    app.run(debug=True)

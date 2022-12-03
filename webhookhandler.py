from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from dotenv import load_dotenv
import os

SQLALCHEMY_TRACK_MODIFICATIONS = False
load_dotenv()

DATABASE_TYPE = os.getenv('DATABASE_TYPE')
HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
PORT = os.getenv('PORT')

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (f"{DATABASE_TYPE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
db = SQLAlchemy(app)



class Event(db.Model):
    __tablename__='changes'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.NVARCHAR('max'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    def __init__(self, data):
      self.data = data

    
@app.route('/')
def root():
  return 'Welcome to CQ Webhook Handler'

@app.route('/github', methods=['POST'])
def webhook():
  print('post received')
  confirm_json = request.headers['content-type'] == 'application/json'
  confirm_push = request.headers['X-Github-Event'] == 'push'
  confirm_main = request.json['ref'] == 'refs/heads/main'
  if confirm_json and confirm_push and confirm_main:
      data = request.json
      event = Event(data)
      db.session.add(event)
      db.session.commit()
      return "Push Data added to Database"         

if __name__ == '__main__':
  app.run(debug=True)
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
import json
import sqlalchemy
import datetime
from dotenv import load_dotenv


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (f"{DATABASE_TYPE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
db = SQLAlchemy(app)



class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Nvarchar('max'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    
@app.route('/')
def root():
  return 'Welcome to CQ Webhook Handler'

@app.route('/github', methods=['POST'])
def webhook():
  print('post received')
  confirm_json = request.headers['content-type'] == 'application/json'
  confirm_push = request.headers['X-Github-Event'] == 'push'
  confirm_post = request.method == 'POST'
  if confirm_json and confirm_push and confirm_post:
      event = request.json
      with open('event.json', 'w') as outfile:
          pass

      with open('event.json', 'a') as outfile:
        json.dump(event, outfile, indent=4)
      return event          

if __name__ == '__main__':
  app.run(debug=True)
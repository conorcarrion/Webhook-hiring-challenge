
# Python Microservice

## Overview

1. Receive webhook calls with events from Github. Only push. Only main branch.
2. Cut down event and upsert to a postgreSQL table
3. pylint
4. dockerfile
5. docker-compose

tips:

1. Ngrok
2. only push, only main
3. Flask
4. unit tests (pytest) monkeypatch/mock
5. SQLalchemy

Bonus:
1. Github actions for Pylint, testing and docker build
2. Deploy to Heroku and connect it to webhooks in github.

### 13:30-15:30 Wednesday 30th Nov

Studying tools required to complete the task:

Familiar:
Docker
PostgreSQL
Github
Unit test + Mock
Github actions

Required reading:
Webhooks
Ngrok
Flask
monkeypatch
Pylint
Heroku

Followed free course: https://www.youtube.com/watch?v=41NOoEz3Tzc
with associated repo: https://github.com/twiliodeved/webhooks-course

This course explained Webhooks, ngrok and cloud function services.

I made a Heroku account and familiarised myself with deploying. 

### Thursday 16:00 - 17:00

Learning flask

free course: https://youtu.be/Z1RJmh_OqeA
repo : https://github.com/jakerieger/FlaskIntroduction

### Friday 21:00-23:00

Using postman, ngrok, flask, sqlalchemy to create app.py. 

@python
```
app = Flask(__name__)
db = SQLAlchemy(app)

@app.route('/github', methods=['POST'])
def webhook():

```

### Saturday 16:30-18:30


Made working version of app.py after troubleshooting env variables and db.create_all(). 

created dockerfile and docker-compose.yml.



docs: https://docs.docker.com/compose/gettingstarted/

### Monday 09:30-11:30

Reading https://flask-testing.readthedocs.io/en/v0.4/ for flask unit testing

Perhaps should use jsonify instead of json_dumps for response. https://www.fullstackpython.com/flask-json-jsonify-examples.html



# Appendix

# <company> Hiring Challenge

Dear future company employee, thank you so much for your interest in joining our team and company. You will be joining a fast growing organisation and be one of the very first people to help us define our culture.

We kindly request you to complete the challenge below, should you be inclined to join us. We estimate it should take between 4 - 8 hours to complete. The objective of this assignment is for us to have an indication of where you are in your journey as a developer, as well as assess your ability to work independently.

## Challenge

Create a new python microservice that will:

- Receive webhook calls with events from GitHub and filter for pushes only on the default branch of the repo - [https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads#push](https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads#push).
- Save a change event to a PostgreSQL table `changes` with fields `id` and `data`, where id is auto-incremented, and data is a JSON field with the following structure:
    
    ```jsx
    {
    	"ts": "<time of the push event>",
      "source": "github",
      "change_type": "push",
      "data": {
        "repository": "repo that was pushed to, ex: head/main",
    		"branch": "name of the branch the changes were pushed to, ex: main",,
        "commit": "commit sha that is the HEAD after the push",
        "author": "Name/email of the author, ex: name <name@company.com>",
        "message": "Last commit message that is not a merge commit",
      }
    }
    ```
    
- Set up pylint and a Dockerfile to build a container for the python microservice
- Set up a `docker-compose.yml` file that starts both the database and the docker container locally
- Publish this code to a private github repository and invite us as an external collaborator for review.

**Some tips**

- Ngrok is a great tool to enable you to develop webhooks while running a process in your machine.
- Not every event from GitHub is a push event, and not every push event is for the main branch.
- Using Flask for the webhook will be easier than FastAPI due to the changing nature of the data structure
- Don't forget to write unit tests! Pytest fixtures are your best friend. If you need to mock functions, look at pytests’ `[monkeypatch](https://docs.pytest.org/en/7.1.x/how-to/monkeypatch.html)` fixture as well as python's standard library `[unittest.mock.Mock](https://docs.python.org/3/library/unittest.mock.html)`
- SQLAlchemy and Alembic are great libraries for interacting with the database and managing its schema respectively

**Bonus points**

- Set up a build using Github Actions that runs the linter, tests and builds the docker container
- Deploy the service to Herkou and connect it to the webhooks in your repository on GitHub. We would love to see a live demo 😉

Good luck, and we look forward to receiving your completed assignment!


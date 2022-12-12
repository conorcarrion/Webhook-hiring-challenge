
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


### Tuesday 19:30-21:30

Testing proving to be a real problem.

https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/contexts/

https://circleci.com/blog/testing-flask-framework-with-pytest/

https://coderpad.io/blog/development/a-guide-to-database-unit-testing-with-pytest-and-sqlalchemy/

https://flask.palletsprojects.com/en/2.2.x/testing/

Made Github action to lint, run testing and make dockerfile. 

Returned to testing, made some progress with the tests but still unsure of pytest fixtures, Flask instantiation and appropriate setup & Teardown.


### Saturday 

Unfortunately during a Ubuntu reinstall my personal documents and my progress on the test_app.py since Wednesday were lost. I believe I still learned a lot and will be able to rewrite it with what I learned, but it is still a setback. 

### Sunday

Worked on learning how to use docker instead of miniconda or virtualenv. Learned how to use volumes. Made changes to dockerfile and docker-compose. 

Almost wrapped up testing, 3/4 passing, last one is due to formatting, need to work out why. 

### Monday 07:30

Not happy with current config setup for database variables. I want to be able to load a different postgres database for testing, development and production. 

Read:
https://www.thedigitalcatonline.com/blog/2020/07/05/flask-project-setup-tdd-docker-postgres-and-more-part-1/

The above project essentially has a config.py file, which has a Base config class and then Production, development and testing config classes which inherit from Base. Then the project uses json files to store environment variables and a script which uses click to do some more clever things. This was a bit too much.

I want to implement removing the environment variables from the docker-compose and only having one: FLASK_CONFIG="development" (or ="testing", or "production". I might even be able to not have it in the compose file at all, I don't know if -> FLASKCONFIG="development" docker compose up   would work.

I also have seen declarative_base() in a few documents and wanted to understand this. 

Read:
https://staskoltsov.medium.com/demystifying-flask-sqlalchemy-a3d8a786ed2f
Seems to be to allow a separation of the model, for example ChangeEvent, from the db=SQLAlchemy() variable/instance, which itself is tied to the 'app' Flask variable/instance. It does this by creating a custom model class. It used to be a third party extension but is now available through: sqlalchemy.ext.declarative import declarative_base.

# Monday 

I have been looking at options to avoid using environment variables and load_dotenv() for the postgres configuration. I have worked out app.config.fromobject and app.config.frompyfile.  

Object could be convenient for something like this:
```
class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DATABASE_URI = "mysql://user@localhost/foo"


class DevelopmentConfig(Config):
    DATABASE_URI = "postgresql+psycopg2://postgres:pgpassword@postgres:5432/postgres"


class TestingConfig(Config):
    DATABASE_URI = "sqlite:///:memory:"
    TESTING = True

```
Which I found in the docs. However the from_object docs say:
from_object(obj)
"You should not use this function to load the actual configuration but rather configuration defaults. The actual config should be loaded with from_pyfile() and ideally from a location not within the package because the package might be installed system wide."

So I am not sure whethey they recommend it or not.

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


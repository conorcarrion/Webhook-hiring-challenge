# Revend Hiring Challenge

Dear future Revendeer, thank you so much for your interest in joining our team and company. You will be joining a fast growing organisation and be one of the very first people to help us define our culture.

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
        "repository": "repo that was pushed to, ex: revendai/isengard",
    		"branch": "name of the branch the changes were pushed to, ex: main",,
        "commit": "commit sha that is the HEAD after the push",
        "author": "Name/email of the author, ex: Alex Reis <alex@revend.ai>",
        "message": "Last commit message that is not a merge commit",
      }
    }
    ```
    
- Set up pylint and a Dockerfile to build a container for the python microservice
- Set up a `docker-compose.yml` file that starts both the database and the docker container locally
- Publish this code to a private github repository and invite user `alexmreis` as an external collaborator for review, or send a zip file of the code (including .git) to `alex@revend.ai`

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

Alex and Peter
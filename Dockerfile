# starting with latest python image
FROM python:latest

# making a directory for the webscraper
RUN mkdir /webhookhandler

# the working directory
WORKDIR /webhookhandler

# add entire contents of this folder to the image
COPY . .

# install library requirements
RUN pip install -r requirements.txt

# execute main.py
ENTRYPOINT ["python3", "webhookhandler.py"]
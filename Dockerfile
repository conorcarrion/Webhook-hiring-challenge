FROM python:latest
RUN mkdir /webhookhandler
WORKDIR /webhookhandler
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY source .
EXPOSE 5000
CMD ["python3", "webhookhandler.py"]
FROM python:latest
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY source .
EXPOSE 5000
CMD ["python3", "app.py"]
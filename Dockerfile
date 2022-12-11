FROM python:latest
RUN mkdir /revend
WORKDIR /revend
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV PYTHONPATH="$PYTHONPATH:/revend"
COPY . .
EXPOSE 5000
CMD ["python", "source/app.py"]
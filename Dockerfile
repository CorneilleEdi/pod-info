FROM python:3.11-alpine3.19

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt && pip cache purge

EXPOSE 8080

ENV FLASK_APP app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]

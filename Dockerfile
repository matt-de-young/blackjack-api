FROM python:3.8-alpine
RUN apk update
RUN apk add --no-cache git gcc musl-dev postgresql-dev libffi-dev
RUN pip install pipenv 

ENV FLASK_APP "api/app.py"

RUN mkdir /app
WORKDIR /app
COPY Pipfile* /app/
RUN pipenv install --system --deploy --ignore-pipfile

CMD flask run --host=0.0.0.0

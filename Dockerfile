FROM python:3.6 as base

RUN mkdir -p /application
WORKDIR /application
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv && pipenv install --ignore-pipfile --system --deploy --dev
COPY . .

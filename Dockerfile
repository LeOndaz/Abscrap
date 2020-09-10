FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /scrapit
WORKDIR /scrapit
COPY requirements/dev.txt .
RUN pip install -r requirements.txt
COPY . /scrapit
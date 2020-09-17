FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /abscrap
WORKDIR /abscrap
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /abscrap
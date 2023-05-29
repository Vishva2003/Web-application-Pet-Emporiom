FROM python:3.10


WORKDIR /app

ADD . /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

RUN pip install mysql-connector-python

EXPOSE 5000

CMD ["python", "app.py"]

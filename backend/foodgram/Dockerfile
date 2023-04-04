FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY . .


ENTRYPOINT ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000" ]
#ENTRYPOINT ["gunicorn", "foodgram.wsgi:application", "--bind", "127.0.0.1:8000" ]
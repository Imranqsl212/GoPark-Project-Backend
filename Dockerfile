FROM python:3.11


WORKDIR /app

COPY . /app/

EXPOSE 8000

RUN pip install --upgrade pip && pip install -r requirements.txt


CMD ["gunicorn"  , "--bind", "0.0.0.0:8000", "backend.wsgi:application"]

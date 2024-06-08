FROM python:3.8-buster

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "--workers", "3", "hub.wsgi:application", "--bind", "0.0.0.0:8000"]

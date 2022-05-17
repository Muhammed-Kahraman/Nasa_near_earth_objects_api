FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate

RUN python manage.py makemigrations

EXPOSE 8000

CMD ["python3", "manage.py", "runserver","0.0.0.0:8000"]

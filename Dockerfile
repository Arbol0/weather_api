
FROM python:3.8-slim

WORKDIR /app

COPY Pipfile* ./

RUN pip install --no-cache-dir pipenv

RUN pipenv install --system --deploy

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

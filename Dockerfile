# Use the official Python image from the Docker Hub
FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./.env  /code/.env

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY alembic.ini /code/alembic.ini

COPY ./alembic /code/alembic

COPY ./app /code/app

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

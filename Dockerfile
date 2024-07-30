FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev

EXPOSE 8000
CMD poetry run fastapi run --host 0.0.0.0 fast_zero/app.py

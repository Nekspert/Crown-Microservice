FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir poetry==2.3.0

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --without dev

COPY app ./app

CMD alembic -c app/alembic.ini upgrade head && python -m app.run

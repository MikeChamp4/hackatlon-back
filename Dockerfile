FROM python:3.11.9

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "app/main.py"]

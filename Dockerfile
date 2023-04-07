FROM python:3.10

WORKDIR /src

COPY pyproject.toml /src/pyproject.toml
COPY poetry.lock /src/poetry.lock

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . /src

CMD ["poetry", "run", "nano/client.py"]

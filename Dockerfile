FROM python:3.12 AS build

WORKDIR /portainer-control

# Виртуальное окружение для slim-версий
COPY pyproject.toml poetry.lock ./
RUN pip install poetry 
RUN poetry self update

RUN python -m venv /venv
RUN . /venv/bin/activate && poetry install --no-root --without dev

FROM python:3.12-slim AS production
COPY . .
COPY --from=build /venv /venv

EXPOSE 8101
ENTRYPOINT [ "/bin/sh", "startup.sh" ]
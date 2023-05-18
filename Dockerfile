FROM python:3.9

WORKDIR /code

# Install poetry and dependencies
RUN pip install poetry
COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the code
COPY . /code/

CMD ["uvicorn", "online_learner_app.fastapi_app:app", "--host", "0.0.0.0", "--port", "80"]
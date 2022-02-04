FROM python:3.10

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_MIN_VERSION=1.0.0

RUN pip install "poetry>=${POETRY_MIN_VERSION}"

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev --no-interaction --no-ansi

COPY .streamlit ./.streamlit
COPY scintigraphy_threshold_area ./scintigraphy_threshold_area
COPY app.py ./

CMD [ "poetry", "run", "streamlit", "run", "app.py" ]

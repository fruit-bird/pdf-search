# Step 1: Base image
FROM python:3.12.5-slim-bookworm as python-base

# Python setup
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

# Step 2: Builder image
FROM python-base as builder

# Install system dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libsqlite3-dev

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy project files
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# Install runtime dependencies
RUN poetry install --without test

# Step 3: Runtime image
FROM python-base as runtime

# Install system dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    libsqlite3-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

# Copy application code
WORKDIR /app
COPY pdf_search/ /app/pdf_search/
COPY config.dev.yaml /app/config.dev.yaml

# Set up entrypoint
CMD ["python", "pdf_search/main.py"]

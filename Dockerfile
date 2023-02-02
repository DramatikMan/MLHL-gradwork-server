FROM python:3.11-slim AS base
WORKDIR /app

# global system
ARG UID=1000
ARG GID=1000

RUN addgroup --system --gid $GID drm \
    && adduser --system --disabled-password --no-create-home --uid $UID --shell /sbin/nologin --ingroup drm --gecos drm drm

##################
FROM base AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.3.2

RUN apt update && apt install --no-install-recommends -y make \
    && rm -rf /var/lib/apt/lists/* \
    && pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.in-project true \
    && mkdir .venv

COPY pyproject.toml poetry.lock* ./
ARG build_env
RUN bash -c 'if [[ "$build_env" == "dev" ]]; then poetry install; else poetry install --only main; fi'
COPY . .
RUN poetry install --only-root

##################
FROM base AS final
RUN chown -R $UID:0 /app && chmod -R g+wx /app
ENV PATH="/app/.venv/bin:/app:$PATH"
COPY --from=builder /app/.venv /app/.venv
COPY server server
USER $UID
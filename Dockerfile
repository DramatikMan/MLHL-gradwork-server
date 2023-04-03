FROM python:3.10-slim AS base
WORKDIR /app

# global system
ARG UID=1000
ARG GID=1000

RUN addgroup --system --gid $GID drm \
    && adduser --system --disabled-password --no-create-home --uid $UID --shell /sbin/nologin --ingroup drm --gecos drm drm \
    && apt update && apt install --no-install-recommends -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

##################
FROM base AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN pip install "pdm==2.4.9" \
    && pdm config check_update false \
    && pdm config venv.in_project true

COPY pyproject.toml pdm.lock* ./
ARG build_env
RUN bash -c 'if [[ "$build_env" == "dev" ]]; then pdm install; else pdm install --prod; fi'
COPY gwserver gwserver

##################
FROM base AS final
ENV PATH="/app/.venv/bin:/app:$PATH"
COPY --from=builder /app/.venv /app/.venv
COPY gwserver gwserver
RUN chown -R $UID:$GID /app && chmod -R ug+wx /app
USER $UID
CMD gwserver start api

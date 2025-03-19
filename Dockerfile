FROM python:3.12

ARG APP_HOME=/opt/rag_app

WORKDIR ${APP_HOME}

RUN pip install uv --no-cache-dir
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY uv.lock .
COPY pyproject.toml .
COPY entrypoint.sh .

RUN --mount=type=cache,target=/root/.cache/uv \
uv sync --frozen --no-dev

COPY app ./app

ENV PATH="${APP_HOME}/.venv/bin:$PATH"
ENV PYTHONPATH=${APP_HOME}

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
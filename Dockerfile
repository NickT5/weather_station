# See uv docs for uv+docker: https://docs.astral.sh/uv/guides/integration/docker/
ARG PYTHON_VERSION="3.12"
FROM python:${PYTHON_VERSION}-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.7 /uv /uvx /bin/

# initialize python venv
WORKDIR /home/pi/app
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --locked

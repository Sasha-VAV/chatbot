FROM python:3.12 AS builder

WORKDIR /app

RUN pip install uv

COPY pyproject.toml README.md ./
RUN mkdir "backend" && touch backend/__init__.py

RUN uv venv -p python3.12 /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN uv pip install .

FROM builder AS dev

WORKDIR /app

RUN apt update && apt install -y vim

COPY . .

FROM python:3.12-slim AS production

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY backend backend

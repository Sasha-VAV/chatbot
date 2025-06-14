FROM python:3.12

WORKDIR /app

RUN pip install uv

COPY pyproject.toml README.md ./
RUN mkdir "backend" && touch backend/__init__.py

RUN uv pip install . --system

COPY backend backend

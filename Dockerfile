# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.8  # Zmiana na wspieraną wersję
FROM python:${PYTHON_VERSION}-slim AS base

# Zmienne środowiskowe dla Pythona
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV XDG_CACHE_HOME=/home/appuser/.cache
ENV TRANSFORMERS_CACHE=/home/appuser/.cache/huggingface

WORKDIR /app

# Utworzenie użytkownika aplikacyjnego
RUN useradd -m -u 1001 -d /home/appuser appuser && \
    mkdir -p ${TRANSFORMERS_CACHE} && \
    chown -R appuser:appuser /home/appuser

# Instalacja zależności systemowych
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Instalacja zależności Pythona z optymalizacją cache
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Zmiana własności katalogu aplikacji
RUN chown -R appuser:appuser /app

# Przełączenie na użytkownika aplikacyjnego
USER appuser

# Kopiowanie kodu źródłowego
COPY --chown=appuser:appuser . .

EXPOSE 8000

# Poprawiona składnia CMD
CMD ["gunicorn", "review_project.wsgi", "--bind=0.0.0.0:8000"]
FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instala curl para baixar o uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instala o uv (gerenciador de pacotes Python moderno e rápido)
# O script de instalação instala em /root/.local/bin
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    /root/.local/bin/uv --version

WORKDIR /app

# Copia arquivos de dependências (pyproject.toml e uv.lock)
COPY pyproject.toml uv.lock ./

# Instala dependências usando uv (sem dependências de dev)
# O uv usa o lock file para garantir reproduzibilidade exata
# Usa o caminho completo do uv para garantir que seja encontrado
RUN /root/.local/bin/uv sync --frozen --no-dev

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    UVICORN_WORKERS=4 \
    UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=8000 \
    UVICORN_LOG_LEVEL=info

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libssl3 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && mkdir -p /app \
    && chown -R appuser:appuser /app

WORKDIR /app

# Copia o ambiente virtual criado pelo uv do stage builder
COPY --from=builder /app/.venv /app/.venv

# Copia código da aplicação
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser pyproject.toml ./

# Muda o WORKDIR para src onde está o main.py
WORKDIR /app/src

# Ajusta permissões do .venv para o appuser
RUN chown -R appuser:appuser /app/.venv

# Adiciona o .venv ao PATH para usar os pacotes instalados
ENV PATH="/app/.venv/bin:${PATH}"

USER appuser

EXPOSE 8000

# Nota: Health checks devem ser gerenciados pelo orquestrador (Kubernetes, Docker Compose, etc.)
# Kubernetes usa livenessProbe e readinessProbe
# Docker Compose pode usar healthcheck na configuração do serviço

CMD ["sh", "-c", "uvicorn main:app --host ${UVICORN_HOST} --port ${UVICORN_PORT} --workers ${UVICORN_WORKERS} --log-level ${UVICORN_LOG_LEVEL} --access-log --no-use-colors --proxy-headers --forwarded-allow-ips='*'"]

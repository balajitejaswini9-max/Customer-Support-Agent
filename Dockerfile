FROM python:3.11-slim

WORKDIR /app

# Dependencies layer — cached unless requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application source
COPY src/ ./src/
COPY knowledge_base/ ./knowledge_base/
COPY frontend/ ./frontend/
COPY tests/ ./tests/
COPY scripts/ ./scripts/
COPY docs/ ./docs/

# Repo metadata required by health/ledger checks and Phase 8 evals
COPY feature_list.json .
COPY session-handoff.md .
COPY docker-compose.yml .
COPY AGENTS.md .
COPY CLAUDE.md .
COPY Dockerfile .
COPY init.sh .

ENV KB_DIR=knowledge_base \
    CHROMA_DIR=/data/chroma \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim

WORKDIR /app

# Dependencies layer — cached unless requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application source
COPY src/ ./src/
COPY knowledge_base/ ./knowledge_base/
COPY tests/ ./tests/

ENV KB_DIR=knowledge_base \
    CHROMA_DIR=/data/chroma \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]

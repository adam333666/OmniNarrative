FROM python:3.11-slim

WORKDIR /app/backend
COPY backend/pyproject.toml ./pyproject.toml
RUN pip install --no-cache-dir fastapi uvicorn[standard] pydantic pydantic-settings sqlalchemy alembic psycopg[binary] httpx litellm
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

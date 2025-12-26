FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml ./
COPY uv.lock ./
RUN uv sync
RUN uv pip install torch --index-url https://download.pytorch.org/whl/cpu

EXPOSE 8000

COPY . .

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile=localhost-key.pem", "--ssl-certfile=localhost.pem"]

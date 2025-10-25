FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml ./
COPY uv.lock ./
RUN uv sync --locked

EXPOSE 8000

COPY . .

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

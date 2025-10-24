FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml ./
COPY uv.lock ./
RUN uv sync --locked

COPY . .

CMD ["uv", "run", "streamlit", "run", "app.py"]

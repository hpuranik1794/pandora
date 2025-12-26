# Pandora

Pandora is a compassionate, privacy-focused AI companion designed to listen, understand and support your mental well-being journey. It provides a safe space for users to express themselves, featuring robust encryption for data at rest and a context-aware chat interface.

![Pandora UI](assets/pandora-landing.png)

## Features

*   **🛡️ Privacy-First Architecture**: All conversation data is encrypted at rest using **Fernet** (AES-128).
*   **🧠 Context-Aware AI**: Powered by **RAG** and conversation history, Pandora remembers past interactions to provide meaningful, personalized support.
*   **🔐 Secure Authentication**: Robust user management system using **Argon2** and **JWT** for session management.

## Tech Stack

### Backend
*   **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
*   **Database**: PostgreSQL with `pgvector` extension
*   **ORM**: SQLAlchemy (Async)
*   **Security**: 
    *   `cryptography` (Fernet/AES-128 encryption)
    *   `passlib` + `argon2-cffi` (Password hashing)
    *   `python-jose` (JWT Authentication)
*   **AI/ML**: 
    *   `ollama` (Model: `gemma3:12b-cloud`)
    *   `transformers` (Embedding: `Qwen/Qwen3-Embedding-0.6B`)

### Frontend
*   **Framework**: React (Vite)
*   **Styling**: Tailwind CSS

## Getting Started

### Prerequisites
*   **Python** 3.10 or higher
*   **Node.js** 18 or higher
*   **PostgreSQL** database (with `pgvector` extension enabled)
*   **Ollama** running locally (or an accessible LLM endpoint)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/pandora.git
cd pandora
```

### 2. Backend Setup
Pandora uses `uv` for fast Python package management.

```bash
cd backend

# Create virtual environment and install dependencies
uv sync

# Create .env file
cp .env.example .env
# Edit .env with your database credentials and secrets
```

**Generate SSL Certificates (Required for HTTPS):**
```bash
# Install mkcert (if not installed)
# Windows (Chocolatey): choco install mkcert
# macOS (Homebrew): brew install mkcert

mkcert -install
mkcert localhost
mv localhost-key.pem localhost.pem backend/
```

**Environment Variables (`.env`):**
Create a `.env` file in the root directory.

```ini
DATABASE_URL=postgresql+asyncpg://user:password@localhost/pandora_db
# Generate using: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your_generated_secret_key
# Generate using: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
ENCRYPTION_KEY=your_generated_fernet_key
OLLAMA_API_KEY=your_ollama_api_key
OLLAMA_MODEL=gemma3:12b-cloud
```

**Run the Backend:**
```bash
uv run uvicorn app.main:app \
  --host 0.0.0.0 --port 8000 \
  --ssl-keyfile=localhost-key.pem \
  --ssl-certfile=localhost.pem \
  --reload
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## Dataset & Acknowledgements

To improve the quality and empathy of responses, Pandora utilizes the **Mental Health Counseling Conversations** dataset for RAG context.

*   **Dataset**: [mental_health_counseling_conversations](https://huggingface.co/datasets/Amod/mental_health_counseling_conversations)
*   **Author**: Amod
*   **Publisher**: Hugging Face

```bibtex
@misc{amod_2024,
	author       = { Amod },
	title        = { mental_health_counseling_conversations (Revision 9015341) },
	year         = 2024,
	url          = { https://huggingface.co/datasets/Amod/mental_health_counseling_conversations },
	doi          = { 10.57967/hf/1581 },
	publisher    = { Hugging Face }
}
```

## 📝 License

This project is licensed under the MIT License.

---

Built with ❤️ by [Harsha Puranik](https://github.com/hpuranik1794)

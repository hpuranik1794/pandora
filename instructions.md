# Pandora — Roadmap & Weekly Goals

🗓️ **Week 1 — Foundation & Design**

**Goal:** Get the architecture, repo, and base environment ready.  
**Focus:** Clarity > speed.

- [ ] Write short 1-page architecture doc (components, data flow, privacy model)
- [ ] Sketch system diagram (frontend ↔ FastAPI ↔ Postgres ↔ LLM)
- [ ] Initialize Git repo: `frontend/`, `backend/`, `docker/`, `docs/`
- [ ] Create `.env.example` with placeholder vars
- [ ] Set up `docker-compose.yml` with Postgres and FastAPI skeleton
- [ ] Verify Postgres connectivity and `pgvector` extension installation
- [ ] Set up pre-commit hooks (black, flake8, isort)
- [x] Push initial commit

🗓️ **Week 2 — Backend Auth & Database**

**Goal:** Users can sign in, and messages can be stored securely.  
**Focus:** Clean, testable backend foundation.

- [ ] Add FastAPI dependencies: `fastapi`, `uvicorn`, `sqlalchemy`, `pgvector`, `pydantic-settings`
- [ ] Create models: `User`, `Conversation`, `Message`, `MessageVector`
- [ ] Implement OAuth2 (Google / GitHub) via `Authlib`
- [ ] Add JWT + refresh token endpoints
- [ ] Create base routes:
  - [ ] `POST /messages`
  - [ ] `GET /conversations`
- [ ] Protect routes with auth middleware
- [ ] Test: sign in → create a conversation → post message → retrieve conversation

🗓️ **Week 3 — Server-Side Embeddings (Core of Option B)**

**Goal:** Embed text on the server and perform similarity search.  
**Focus:** Correctness and latency.

- [ ] Add embedding client (Ollama or OpenAI Embeddings API)
- [ ] On `POST /messages`:
  - [ ] Generate embedding
  - [ ] Store vector in `message_vectors`
- [ ] Implement similarity search via `pgvector` (`ORDER BY embedding <=> query_vector`)
- [ ] Build basic RAG pipeline:
  - [ ] Retrieve top-k messages
  - [ ] Construct context + user prompt
  - [ ] Call LLM → generate reply
  - [ ] Store both message and embedding
- [ ] Test end-to-end:
  - [ ] Send message → embedding stored
  - [ ] RAG retrieves relevant past messages

🗓️ **Week 4 — Frontend MVP (Chat UI)**

**Goal:** Get a minimal chat interface working end-to-end.  
**Focus:** Functionality > polish.

- [ ] Create React app (Vite + TypeScript)
- [ ] Set up routing + context for auth
- [ ] Implement:
  - [ ] Message list
  - [ ] Input bar + send button
  - [ ] Streaming message replies (SSE or WebSocket)
- [ ] Integrate OAuth login flow with backend
- [ ] Connect to FastAPI endpoints
- [ ] Test: login → send message → see LLM reply in UI

🗓️ **Week 5 — Security & Privacy Hardening**

**Goal:** Protect user data and lock down backend.  
**Focus:** Real-world privacy and safety.

- [ ] Enable HTTPS (reverse proxy via Caddy or Nginx in Docker)
- [ ] Enforce Row-Level Security (RLS) in Postgres
- [ ] Store JWT in HTTP-only cookies
- [ ] Encrypt at rest (Postgres volume)
- [ ] Implement rate limiting (per IP/user)
- [ ] Sanitize prompts for prompt injection
- [ ] Test: unauthorized user cannot access another’s messages

🗓️ **Week 6 — Safety, Ethics & User Trust**

**Goal:** Handle sensitive cases responsibly.  
**Focus:** Empathy, safety, compliance.

- [ ] Implement crisis detection (keywords or classifier)
- [ ] Display hotline message on detection
- [ ] Add disclaimer and privacy consent screen
- [ ] Add content moderation filters
- [ ] Store consent timestamp in `users` table
- [ ] Test: “I want to hurt myself” → triggers safety prompt

🗓️ **Week 7 — Testing, CI/CD & Deployment**

**Goal:** Prepare for production-like environment.  
**Focus:** Reliability and automation.

- [ ] Write unit tests (auth, message insert, embeddings, RAG)
- [ ] Add integration tests (full chat cycle)
- [ ] Set up GitHub Actions:
  - [ ] Lint + test backend
  - [ ] Build + deploy Docker images
- [ ] Deploy to staging server
- [ ] Verify TLS and correct CORS config
- [ ] Smoke test full flow: login → chat → reply → logout

🗓️ **Week 8 — Polish, Monitoring & Beta Prep**

**Goal:** Refine, measure, and prepare to demo/test.  
**Focus:** Finishing touches.

- [ ] Add conversation search (exact + semantic)
- [ ] Export chat history (encrypted ZIP)
- [ ] Integrate Sentry for monitoring
- [ ] Add privacy-friendly usage metrics
- [ ] Set up nightly encrypted DB backups
- [ ] Write README + architecture doc updates
- [ ] Run mini beta with a few users 🚀

🏁 Done When

- [ ] Users can log in securely
- [ ] Messages stored + embedded on server
- [ ] Relevant context retrieved with `pgvector`
- [ ] LLM replies streamed in real time
- [ ] Safety and privacy features pass tests
- [ ] Deployment reproducible with one command

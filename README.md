# Pandora

Mental health chatbot powered by AI.

Setup

Rebuild docker image and start container
```
docker compose up --build -d
```

For local dev (inside `/backend`)
```
uv run uvicorn app.main:app --port 8000
```


Test endpoints
```
curl -X GET  http://localhost:8000/chat/conversations
curl -X POST  http://localhost:8000/chat/conversations
curl -X GET  http://localhost:8000/chat/message/1

curl -X POST  http://localhost:8000/chat/message/1 \
 -H "Content-type: application/json" \
 -d '{"user_input": "I have been feeling stressed lately."}'

 curl -X POST  http://localhost:8000/chat/message/1 \
 -H "Content-type: application/json" \
 -d '{"user_input": "Yes, I have tried meditation but the kind of work I do makes it hard to focus. It seems like I am always thinking of about work or just stressing out. What else can I do to manage my stress?"}'

curl -X POST  http://localhost:8000/chat/message/1 \
 -H "Content-type: application/json" \
 -d '{"user_input": "I love cubing so I try to do that when I can. It calms the nerves a bit."}'

curl -X POST  http://localhost:8000/chat/message/1 \
 -H "Content-type: application/json" \
 -d '{"user_input": "I have also started going for walks in the evening. It helps clear my mind."}'

curl -X POST  http://localhost:8000/chat/message/1 \
 -H "Content-type: application/json" \
 -d '{"user_input": "Despite all this, I still get panic attacks occasionally. They are quite overwhelming."}'

curl -X POST  http://localhost:8000/chat/message/1 \
 -H "Content-type: application/json" \
 -d '{"user_input": "What are some coping mechanisms do you think I can use?"}'

curl -X POST  http://localhost:8000/chat/message/1 \
  -H "Content-type: application/json" \
  -d '{"user_input": "I have tried deep breathing exercises, yoga, journaling, talking to a friend or family member about my feelings but they seem to be futile. Help me mate!"}'
```

Debug in docker container
```
docker compose logs backend --tail 100
```

Progress:
✅ Create and manage multiple chat sessions
✅ Send and store messages
✅ Talk to your LLM via Docker
✅ Persist everything to SQLite
✅ Basic rag pipeline with conversation embeddings
✅ Limit model response length (user prompt or model config)
✅ Improve embedding storage
⚙️ Add a ton of mental health convos for better context
⚙️ Reduce model response time (research streaming APIs)

Findings
- Embedding creation and retrievals are quick
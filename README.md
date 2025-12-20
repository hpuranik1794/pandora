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

Start frontend
```
npm run dev
```

Test endpoints
```
curl -X GET  http://localhost:8000/chat/conversations
curl -X POST  http://localhost:8000/chat/conversations
curl -X GET  http://localhost:8000/chat/message/1

curl -X POST  http://localhost:8000/chat/message/1 \
 -H "Content-type: application/json" \
 -d '{"user_input": "I have been feeling stressed lately at work."}'

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


------------------------------

[NEW]
curl -X POST  http://localhost:8000/chat/message/1 \
 -H "Content-type: application/json" \
 -d '{"user_input": "I have been really stressed because my workload keeps piling up."}'

curl -X POST http://localhost:8000/chat/message/1 \
  -H "Content-type: application/json" \
  -d '{"user_input": "The stress is arising mostly due to deadlines and the feeling like I am always behind."}'

curl -X POST http://localhost:8000/chat/message/1 \
  -H "Content-type: application/json" \
  -d '{"user_input": "Yes, I have talked to family and friends. They are supportive but I feel like they dont really understand the pressure I am under at work. All they say is to take breaks but that is easier said than done."}'


curl -X POST http://localhost:8000/chat/message/1 \
  -H "Content-type: application/json" \
  -d '{"user_input": "Some of my coworkers left the team and all of their work has now been dumped on me. I have been assigned a lot of new projects with tight deadlines. I feel like I am constantly playing catch up and there is no end in sight."}'
```

Debug in docker container
```
docker compose logs backend --tail 100
```

Progress:
✅ CRUD chat sessions
✅ CRUD messages
✅ Talk to LLM via Docker
✅ Persist everything to SQLite
✅ Basic rag pipeline with user embeddings
✅ Limit model response length (user prompt or model config)
✅ Improve embedding storage
✅ Store user and assistant messages together?
    Soln: turn_id (uuid/int): same turn_id for the user message and the assistant reply so you can treat them as a pair when needed.

✅ Improve model prompt
  1) Make the system message do all instruction/formatting
    Keep your “rules” there (tone, word limit, safety, style).
  2) Use the user message for:
    (Optional) a compact “memory/context” section
    the user’s new message
  3) Enforce a simple response template
    Small models do better when you specify a predictable structure.
✅ Improve rag by filtering recent and relevant messages and getting both user and assistant messages from those turns.

Model/backend improvements planned:
⚙️ Move to a larger LM (7B+)
⚙️ Reduce model response time (research streaming APIs)
⚙️ Add mental health convos for better context (always wrap retrieved content with a "this is general info" system instruction)
⚙️ Migrate to postgres?

Next steps:
✅ Frontend UI (React)
⚙️ Improve UI 
  - improve color scheme
  - add landing page
  - make it SaaS like with login/signup


Findings
- Embedding creation and retrievals are quick
- Small models are not good at following complex instructions, even formatting ones. Improved the prompt but it seems like I've hit the small model ceiling. But it's good enough for now.
- Can improve RAG pipeline by adding mental health specific convos to the DB for better context retrieval. But issues lie in 
  - parroting dataset style instead of being grounded in the user's context
  - can include bad advice, mismatched tone or unsafe content.

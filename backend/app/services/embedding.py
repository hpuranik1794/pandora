from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import torch
import numpy as np


tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-Embedding-0.6B")
model = AutoModel.from_pretrained("Qwen/Qwen3-Embedding-0.6B")

async def embed_text(text: str):
  inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
  with torch.no_grad():
    outputs = model(**inputs)
    # assume it returns last_hidden_state; you'll need pooling
    embedding = outputs.last_hidden_state[:,0,:].cpu().numpy()

  return embedding.flatten().tolist()



async def get_relevant_messages(conversation_id: int, query: str, top_k=2):
  from app.db.crud import get_messages
  
  all_msgs = await get_messages(conversation_id)

  if not all_msgs:
    return []

  all_msgs = sorted(all_msgs, key=lambda m: (m.timestamp, m.id))

  turns = dict()  # turn_id -> {"user": msg dict, "assistant": msg dict}
  for m in all_msgs:
    if m.turn_id is None:
      continue

    bucket = turns.setdefault(m.turn_id, {"user": None, "assistant": None, "ts": None})
    bucket[m.role] = m
    if m.role == "user":
      bucket["ts"] = (m.timestamp, m.id)

  # recent turn ids
  recent_turn_ids = []
  if turns:
    last_turn_id = max(turns.keys(), key=lambda tid: turns[tid]["ts"] if turns[tid]["ts"] else (0, 0))
    recent_turn_ids.append(last_turn_id)

  # retrieve user embeddings
  q_emb = np.array(await embed_text(query))
  scored = []
  for tid, pair in turns.items():
    user_msg = pair.get("user")
    if not user_msg or not user_msg.embedding:
      continue
    
    u_emb = np.array(user_msg.embedding)
    score = cosine_similarity([q_emb], [u_emb])[0][0]
    scored.append((score, tid))

  scored.sort(reverse=True)

  # pick top k turns
  relevant_turn_ids = []
  for score, tid in scored:
    if tid in recent_turn_ids:
      continue

    relevant_turn_ids.append(tid)

    if len(relevant_turn_ids) >= top_k:
      break

  chosen = set(recent_turn_ids + relevant_turn_ids)
  chosen = sorted(chosen, key=lambda tid: turns[tid]["ts"] if turns[tid]["ts"] else (0, 0))

  context = []
  for tid in chosen:
    pair = turns[tid]
    u = pair.get("user")
    a = pair.get("assistant")
    
    if u:
      context.append({"role": "user", "content": u.content})
    if a:
      context.append({"role": "assistant", "content": a.content})

  return context

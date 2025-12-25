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



async def get_rag_context(query_emb: list, top_k: int = 2):
  from app.db.database import database
  
  # Find similar user messages in the RAG dataset
  # We use the <=> operator for cosine distance
  sql = """
    SELECT turn_id
    FROM rag_messages
    WHERE role = 'user'
    ORDER BY embedding_vec <=> :embedding
    LIMIT :limit
  """
  
  # Convert list to string format '[1,2,3]' for pgvector
  embedding_str = str(query_emb)
  
  try:
    rows = await database.fetch_all(query=sql, values={"embedding": embedding_str, "limit": top_k})
  except Exception as e:
    print(f"Error querying RAG messages: {e}")
    return []
      
  if not rows:
    return []
      
  turn_ids = [r["turn_id"] for r in rows]
  
  if not turn_ids:
    return []
      
  # Fetch both user and assistant messages for these turns
  tids_str = ",".join(map(str, turn_ids))
  sql_msgs = f"""
    SELECT role, content, turn_id
    FROM rag_messages
    WHERE turn_id IN ({tids_str})
    ORDER BY turn_id, id
  """
  
  rag_rows = await database.fetch_all(query=sql_msgs)
  
  msgs_by_turn = {}
  for r in rag_rows:
    if r["turn_id"] not in msgs_by_turn:
      msgs_by_turn[r["turn_id"]] = []
    msgs_by_turn[r["turn_id"]].append(r)
      
  rag_context = []
  for tid in turn_ids:
    msgs = msgs_by_turn.get(tid, [])
    # Ensure User comes before Assistant
    u = next((m for m in msgs if m["role"] == "user"), None)
    a = next((m for m in msgs if m["role"] == "assistant"), None)
    
    if u:
      rag_context.append({"role": "user", "content": u["content"]})
    if a:
      rag_context.append({"role": "assistant", "content": a["content"]})
          
  return rag_context


async def get_relevant_messages(conversation_id: int, query: str, top_k=2):
  from app.db.crud import get_messages
  
  # 1. Get embedding for the query
  q_emb = await embed_text(query)
  
  # 2. Get RAG context (similar past conversations from dataset)
  rag_context = await get_rag_context(q_emb, top_k=top_k)
  
  # 3. Get relevant history from current conversation
  all_msgs = await get_messages(conversation_id)

  if not all_msgs:
    return rag_context

  all_msgs = sorted(all_msgs, key=lambda m: (m["timestamp"], m["id"]))

  turns = dict()  # turn_id -> {"user": msg dict, "assistant": msg dict}
  for m in all_msgs:
    if m["turn_id"] is None:
      continue

    bucket = turns.setdefault(m["turn_id"], {"user": None, "assistant": None, "ts": None})
    bucket[m["role"]] = m
    if m["role"] == "user":
      bucket["ts"] = (m["timestamp"], m["id"])

  # recent turn ids
  recent_turn_ids = []
  if turns:
    last_turn_id = max(turns.keys(), key=lambda tid: turns[tid]["ts"] if turns[tid]["ts"] else (0, 0))
    recent_turn_ids.append(last_turn_id)

  # retrieve user embeddings
  q_emb_np = np.array(q_emb)
  scored = []
  for tid, pair in turns.items():
    user_msg = pair.get("user")
    if not user_msg or not user_msg.get("embedding"):
      continue
    
    u_emb = np.array(user_msg["embedding"])
    score = cosine_similarity([q_emb_np], [u_emb])[0][0]
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

  history_context = []
  for tid in chosen:
    pair = turns[tid]
    u = pair.get("user")
    a = pair.get("assistant")
    
    if u:
      history_context.append({"role": "user", "content": u["content"], "source": "history"})
    if a:
      history_context.append({"role": "assistant", "content": a["content"], "source": "history"})

  # Mark RAG context source
  for msg in rag_context:
      msg["source"] = "rag"

  # Combine: RAG context first, then history
  return rag_context + history_context

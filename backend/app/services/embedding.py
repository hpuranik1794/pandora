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



async def get_relevant_messages(conversation_id: int, query: str, top_k=3):
  from app.db.crud import get_messages
  
  query_embedding = np.array(await embed_text(query))
  messages = await get_messages(conversation_id)

  scored = []
  for m in messages:
    if m.embedding:
      score = cosine_similarity([query_embedding], [m.embedding])[0][0]
      scored.append((score, m.content))

  scored.sort(reverse=True)
  
  return [m for _, m in scored[:top_k]]



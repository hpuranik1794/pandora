from typing import Generator
from ollama import Client
from dotenv import load_dotenv
import os

load_dotenv()

client = Client(
  host="https://ollama.com",
  headers={'Authorization': 'Bearer ' + os.getenv('OLLAMA_API_KEY')}
)


def build_prompt(user_input, context_messages):
  rag_section = ""
  history_section = ""

  if context_messages:
    rag_msgs = [m for m in context_messages if m.get("source") == "rag"]
    history_msgs = [m for m in context_messages if m.get("source") == "history"]

    if rag_msgs:
      rag_text = "\n".join([f"- {msg['role'].upper()}: {msg['content']}" for msg in rag_msgs])
      rag_section = f"Reference examples (similar past conversations):\n{rag_text}\n\n"
    
    if history_msgs:
      hist_text = "\n".join([f"- {msg['role'].upper()}: {msg['content']}" for msg in history_msgs])
      history_section = f"Current conversation history (most relevant):\n{hist_text}\n\n"

  return f"{rag_section}{history_section}New user message:\n{user_input}\n"


def generate_response(user_input: str, context_messages: list = []) -> Generator[str, None, None]:
  system_instructions = """
  You are a supportive mental health assistant. Be warm, validating, and practical.
  Do not claim you've seen/heard/know the user unless it is explicitly in the provided context.
  Avoid repeating the same question or generic reassurance when the user adds new details.
  Do not use metaphors involving ledges or harm. Use neutral language.
  Do not claim you are a therapist or provide medical diagnosis.
  If the user mentions self-harm or suicide, respond briefly and encourage reaching out to local emergency services or a trusted person.
  Your question must reference a concrete detail the user mentioned. Avoid generic "tell me more".
  Keep your response <= 80 words.
  
  Output EXACTLY 3 lines:
  Validation (one sentence).
  Question (one specific question about the user's situation).
  Suggestion (one small, concrete next step phrased as a statement).
  No extra lines, no bullet points, no paragraphs.
  """.strip()

  prompt = build_prompt(user_input, context_messages)

  response = client.chat(
    model=os.getenv("OLLAMA_MODEL"), 
    messages=[
      {"role": "system", "content": system_instructions},
      {"role": "user", "content": prompt}
    ],
    options={
      "num_predict": 110
    },
    stream=True)

  for part in response:
    yield part.message.content



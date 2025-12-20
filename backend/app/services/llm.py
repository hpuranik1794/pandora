from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))

def build_prompt(user_input, context_messages):
  if context_messages:
    context_text = "\n".join([f"- {msg['role'].upper()}: {msg['content']}" for msg in context_messages])
    context_block = f"Prior context (most relevant, in order):\n{context_text}\n"
  else:
    context_block = "Prior context: (none)\n"

  return f"{context_block}New user message:\n{user_input}\n"


async def generate_response(user_input: str, context_messages: list) -> str:
  system_instructions = """
  You are a supportive mental health assistant. Be warm, validating, and practical.
  Do not claim you've seen/heard/know the user unless it is explicitly in the provided context.
  Avoid repeating the same question or generic reassurance when the user adds new details.
  Do not use metaphors involving ledges or harm. Use neutral language.
  Do not claim you are a therapist or provide medical diagnosis.
  If the user mentions self-harm or suicide, respond briefly and encourage reaching out to local emergency services or a trusted person.
  Your question must reference a concrete detail the user mentioned. Avoid generic "tell me more".
  Keep your response <= 80 words.
  
  Output EXACTLY 3 lines, using these exact prefixes:
  Validation: (one sentence).
  Question: (one specific question about the user's situation).
  Suggestion: (one small, concrete next step).
  No extra lines, no bullet points, no paragraphs.
  """.strip()

  prompt = build_prompt(user_input, context_messages)

  response = client.chat.completions.create(
    model=os.getenv("MODEL_NAME"),
    messages=[
      {"role": "system", "content": system_instructions},
      {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=110
  )

  return response.choices[0].message.content



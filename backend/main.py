import requests

url = "http://localhost:12434/engines/llama.cpp/v1/chat/completions"

data = {
  "model": "ai/smollm2",
  "messages": [
    {
      "role": "system",
      "content": "You are a compassionate mental health assistant."
    },
    {
      "role": "user",
      "content": "I'm feeling really overwhelmed with everything going on in my life."
    }
  ]
}

response = requests.post(url, json=data)
response.raise_for_status()

print(response.json()["choices"][0]["message"]["content"])
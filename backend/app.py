import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))

st.title("Compassionate Mental Health Assistant")
prompt = st.text_area("Describe how you're feeling:")

if st.button("Get Support"):
  with st.spinner("Generating help..."):
    if prompt:
        messages = [
          {"role": "system", "content": "You are a compassionate mental health assistant."},
          {"role": "user", "content": prompt}
        ]
        
        response = client.chat.completions.create(
          model=os.getenv("MODEL_NAME"),
          messages=messages
        )
        
        st.success(f"Response: \n{response.choices[0].message.content}")
    else:
        st.warning("Please enter a description of how you're feeling.")

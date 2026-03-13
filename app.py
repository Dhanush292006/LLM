import streamlit as st
from transformers import pipeline

st.title("AI Chatbot")

chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

prompt = st.text_input("Ask something")

if prompt:
    result = chatbot(prompt, max_length=100)
    st.write(result[0]["generated_text"])

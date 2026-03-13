import streamlit as st
import pandas as pd
from transformers import pipeline

st.title("CSV LLM Chatbot")

# Load dataset
df = pd.read_csv("GPT DATA COLLECTION(Sheet1).csv")

# Load model
chatbot = pipeline("text-generation", model="gpt2")

user_input = st.text_input("Ask a question")

if user_input:
    response = chatbot(user_input, max_length=100)
    st.write(response[0]['generated_text'])

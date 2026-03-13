import streamlit as st
import pandas as pd
from transformers import pipeline

st.title("CSV Chatbot")

df = pd.read_csv("GPT DATA COLLECTION(Sheet1).csv")

chatbot = pipeline("text-generation", model="gpt2")

question = st.text_input("Ask something")

if question:
    response = chatbot(question, max_length=50)
    st.write(response[0]["generated_text"])

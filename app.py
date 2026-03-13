import streamlit as st
import ollama

st.title("Local ChatGPT with Ollama")

prompt = st.chat_input("Ask something")

if prompt:
    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user","content":prompt}]
    )

    st.write(response["message"]["content"])

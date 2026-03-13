import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="AIzaSyD4ATJfp6fHEPyDjOZWurs--09eEzOhH2o")

st.title("My AI Assistant")

user_input = st.text_input("Ask anything")

if user_input:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":user_input}]
    )

    st.write(response.choices[0].message.content)

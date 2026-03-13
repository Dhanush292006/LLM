import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="AIzaSyDFN-L5LZ1uLJ5ohts3x5hn0uf9kZ2TrdE")

st.title("My AI Assistant")

user_input = st.text_input("Ask anything")

if user_input:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":user_input}]
    )

    st.write(response.choices[0].message.content)

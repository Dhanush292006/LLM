import streamlit as st
from transformers import pipeline

st.title("🤖 ChatGPT Style AI (No API Key)")

@st.cache_resource
def load_model():
    generator = pipeline(
        "text-generation",
        model="distilgpt2"
    )
    return generator

model = load_model()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask something")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    response = model(prompt, max_new_tokens=60)

    answer = response[0]["generated_text"]

    # remove prompt text
    answer = answer.replace(prompt, "").strip()

    if answer == "":
        answer = "I am thinking... please try another question."

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)

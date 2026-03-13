import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="ChatGPT Clone")

st.title("🤖 Local LLM Chatbot")

@st.cache_resource
def load_model():
    model = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    )
    return model

llm = load_model()

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# user input
prompt = st.chat_input("Ask something")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    result = llm(prompt, max_new_tokens=120)

    answer = result[0]["generated_text"]

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.write(answer)

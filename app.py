import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="ChatGPT Clone")

st.title("🤖 ChatGPT Style AI (No API Key)")

@st.cache_resource
def load_model():
    generator = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    )
    return generator

model = load_model()

# chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# display old messages
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

    # generate response
    result = model(
        prompt,
        max_new_tokens=80,
        do_sample=True,
        temperature=0.7
    )

    answer = result[0]["generated_text"]

    # remove prompt from output
    answer = answer.replace(prompt, "").strip()

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.write(answer)

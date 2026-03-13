import streamlit as st
from openai import OpenAI
import pandas as pd
from pypdf import PdfReader

# Page settings
st.set_page_config(page_title="ChatGPT File Assistant", layout="wide")

st.title("🤖 ChatGPT File Assistant")

# =========================
# API KEY
# =========================

api_key = st.text_input("Enter OpenAI API Key", type="password")

client = None
if api_key:
    client = OpenAI(api_key=api_key)

# =========================
# SESSION MEMORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# FILE UPLOAD
# =========================

st.sidebar.title("Upload File")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV / TXT / PDF",
    type=["csv", "txt", "pdf"]
)

file_data = ""

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)
        file_data = df.to_string()

        st.sidebar.write("Dataset Preview")
        st.sidebar.dataframe(df.head())


    elif uploaded_file.name.endswith(".txt"):

        file_data = uploaded_file.read().decode()


    elif uploaded_file.name.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        for page in reader.pages:

            text = page.extract_text()

            if text:
                file_data += text

# =========================
# SHOW CHAT HISTORY
# =========================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# CHAT INPUT
# =========================

prompt = st.chat_input("Ask something...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Default reply
    reply = ""

    if client is None:

        reply = "⚠️ Please enter your OpenAI API key."

    else:

        if file_data != "":

            system_prompt = f"""
You are a helpful AI assistant.

Answer using the uploaded file data if possible.

FILE DATA:
{file_data}
"""

        else:

            system_prompt = "You are a helpful AI assistant."

        try:

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )

            reply = response.choices[0].message.content

        except Exception as e:

            reply = "⚠️ API error or quota exceeded. Please check OpenAI billing."

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

import streamlit as st
from openai import OpenAI
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="ChatGPT Clone", layout="wide")

st.title("🤖 ChatGPT Clone")

# API KEY
api_key = st.text_input("Enter OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar upload
st.sidebar.title("Upload File")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV / PDF / TXT",
    type=["csv", "txt", "pdf"]
)

file_data = ""

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        file_data = df.to_string()
        st.sidebar.dataframe(df.head())

    elif uploaded_file.name.endswith(".txt"):
        file_data = uploaded_file.read().decode()

    elif uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                file_data += text

# Display chat history
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Ask something...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    if file_data != "":
        system_prompt = f"""
        Answer using the uploaded file if possible.

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
    reply = "⚠️ API quota exceeded or API key problem."

st.write(reply)

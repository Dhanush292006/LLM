import streamlit as st
import pandas as pd
import google.generativeai as genai
from pypdf import PdfReader

st.set_page_config(page_title="Gemini Chat Assistant", layout="wide")

st.title("🤖 Gemini Chat Assistant")

# API key
api_key = st.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar upload
st.sidebar.title("Upload File")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV / TXT / PDF",
    type=["csv","txt","pdf"]
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

# Show chat history
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Ask something...")

if prompt:

    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    if api_key:

        if file_data != "":
            query = f"""
Use this file data to answer if possible:

{file_data}

Question:
{prompt}
"""
        else:
            query = prompt

        response = model.generate_content(query)

        reply = response.text

    else:
        reply = "⚠️ Please enter Gemini API key."

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append(
        {"role":"assistant","content":reply}
    )

import streamlit as st
import google.generativeai as genai
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="AI Chat", layout="wide")

st.title("🤖 AI Chat Assistant")

# =========================
# API KEY
# =========================

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

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
    type=["csv","txt","pdf"]
)

file_text = ""

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)
        file_text = df.to_string()

        st.sidebar.dataframe(df.head())

    elif uploaded_file.name.endswith(".txt"):

        file_text = uploaded_file.read().decode()

    elif uploaded_file.name.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        for page in reader.pages:

            txt = page.extract_text()

            if txt:
                file_text += txt

# =========================
# SHOW CHAT HISTORY
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# CHAT INPUT
# =========================

prompt = st.chat_input("Send a message...")

if prompt:

    st.session_state.messages.append(
        {"role":"user","content":prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:

        reply = "⚠️ Please enter Gemini API key."

    else:

        if file_text != "":

            query = f"""
Use the following data to answer if possible.

DATA:
{file_text}

Question:
{prompt}
"""

        else:

            query = prompt

        try:

            response = model.generate_content(query)

            reply = response.text

        except:

            reply = "⚠️ Error generating response."

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append(
        {"role":"assistant","content":reply}
    )

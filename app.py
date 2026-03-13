import streamlit as st
import google.generativeai as genai
import pandas as pd
from pypdf import PdfReader

# Page settings
st.set_page_config(page_title="Gemini File Assistant", layout="wide")

st.title("♊ Gemini File Assistant")

# =========================
# API KEY & SETUP
# =========================

api_key = st.text_input("import streamlit as st
import google.generativeai as genai
import pandas as pd
from pypdf import PdfReader

# Page settings
st.set_page_config(page_title="Gemini File Assistant", layout="wide")

st.title("♊ Gemini File Assistant")

# =========================
# API KEY & SETUP
# =========================

api_key = st.text_input("Enter Google API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Using gemini-1.5-flash for speed and cost-efficiency
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# =========================
# SESSION MEMORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# FILE UPLOAD (Logic remains mostly the same)
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

prompt = st.chat_input("Ask Gemini something...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    if model is None:
        reply = "⚠️ Please enter your Google API key."
    else:
        # Construct the context
        context = f"Context from uploaded file:\n{file_data}\n\n" if file_data else ""
        full_prompt = f"{context}User Question: {prompt}"

        try:
            # Generate response
            response = model.generate_content(full_prompt)
            reply = response.text
        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Using gemini-1.5-flash for speed and cost-efficiency
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# =========================
# SESSION MEMORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# FILE UPLOAD (Logic remains mostly the same)
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

prompt = st.chat_input("Ask Gemini something...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    if model is None:
        reply = "⚠️ Please enter your Google API key."
    else:
        # Construct the context
        context = f"Context from uploaded file:\n{file_data}\n\n" if file_data else ""
        full_prompt = f"{context}User Question: {prompt}"

        try:
            # Generate response
            response = model.generate_content(full_prompt)
            reply = response.text
        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

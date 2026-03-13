import streamlit as st
import google.generativeai as genai
import pandas as pd
from pypdf import PdfReader

# =========================
# 1. PAGE CONFIGURATION
# =========================
st.set_page_config(page_title="Gemini File Assistant", layout="wide", page_icon="♊")

st.title("♊ Gemini File Assistant")
st.markdown("Upload a file and ask questions about its content using Google Gemini.")

# =========================
# 2. API KEY SETUP
# =========================
# Sidebar for API Key to keep the main area clean
with st.sidebar:
    st.title("Settings ⚙️")
    api_key = st.text_input("Enter Google API Key", type="password", help="Get your key from https://aistudio.google.com/")
    
    if api_key:
        genai.configure(api_key=api_key)
        # Using gemini-1.5-flash for high speed and large context window
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        model = None
        st.info("🔑 Please enter your API key to enable the chat.")

# =========================
# 3. SESSION STATE (Memory)
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# 4. FILE UPLOAD & PROCESSING
# =========================
st.sidebar.divider()
st.sidebar.title("Upload File 📄")
uploaded_file = st.sidebar.file_uploader(
    "Support: CSV, TXT, PDF",
    type=["csv", "txt", "pdf"]
)

# Variable to hold all extracted text
file_context = ""

if uploaded_file:
    with st.spinner("Processing file..."):
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            file_context = df.to_string()
            st.sidebar.write("✅ CSV Loaded")
            st.sidebar.dataframe(df.head(5))

        elif uploaded_file.name.endswith(".txt"):
            file_context = uploaded_file.read().decode()
            st.sidebar.write("✅ Text Loaded")

        elif uploaded_file.name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    file_context += text
            st.sidebar.write("✅ PDF Loaded")

# =========================
# 5. CHAT INTERFACE
# =========================

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Ask a question about your file...")

if prompt:
    # 1. Add user message to state and UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate response
    if model is None:
        reply = "⚠️ API Key is missing. Please provide it in the sidebar."
    else:
        with st.chat_message("assistant"):
            try:
                # Combine file context with the user's prompt
                if file_context:
                    full_query = f"Context from uploaded file:\n{file_context}\n\nUser Question: {prompt}"
                else:
                    full_query = prompt

                response = model.generate_content(full_query)
                reply = response.text
                st.markdown(reply)
                
            except Exception as e:
                reply = f"❌ Error: {str(e)}"
                st.error(reply)

    # 3. Add assistant reply to history
    st.session_state.messages.append({"role": "assistant", "content": reply})

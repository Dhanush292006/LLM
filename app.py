import streamlit as st
import google.generativeai as genai
import pandas as pd
from pypdf import PdfReader

# ==========================================
# 1. PAGE SETUP & UI
# ==========================================
st.set_page_config(page_title="Gemini AI Assistant", layout="wide", page_icon="♊")

st.title("♊ Gemini File Assistant")
st.info("Upload a document (PDF, TXT, or CSV) and chat with Gemini about it.")

# ==========================================
# 2. SIDEBAR: API KEY & FILE UPLOAD
# ==========================================
with st.sidebar:
    st.header("Configuration")
    
    # Secure API Key Input
    api_key = st.text_input("AIzaSyD4ATJfp6fHEPyDjOZWurs--09eEzOhH2o", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        # Using Gemini 1.5 Flash for speed and massive context window
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        model = None
        st.warning("🔑 Please enter an API Key to start.")

    st.divider()
    
    # File Uploader
    st.header("Upload Data")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a file", 
        type=["csv", "txt", "pdf"]
    )

# ==========================================
# 3. FILE PROCESSING LOGIC
# ==========================================
file_content = ""

if uploaded_file:
    with st.spinner("Reading file..."):
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
                file_content = df.to_string()
                st.sidebar.success("CSV Loaded!")
                st.sidebar.dataframe(df.head(3))

            elif uploaded_file.name.endswith(".txt"):
                file_content = uploaded_file.read().decode("utf-8")
                st.sidebar.success("Text Loaded!")

            elif uploaded_file.name.endswith(".pdf"):
                reader = PdfReader(uploaded_file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        file_content += text
                st.sidebar.success("PDF Loaded!")
        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")

# ==========================================
# 4. CHAT HISTORY & SESSION STATE
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 5. CHAT INPUT & AI RESPONSE
# ==========================================
if prompt := st.chat_input("Ask me anything about the file..."):
    
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Assistant response
    with st.chat_message("assistant"):
        if not model:
            response_text = "⚠️ Please provide a valid Google API Key in the sidebar."
            st.error(response_text)
        else:
            try:
                # Prepare context
                if file_content:
                    full_prompt = f"System: Use the following file data to answer the user.\n\nFile Data:\n{file_content}\n\nUser Question: {prompt}"
                else:
                    full_prompt = prompt
                
                # Call Gemini
                response = model.generate_content(full_prompt)
                response_text = response.text
                st.markdown(response_text)
                
            except Exception as e:
                response_text = f"❌ API Error: {str(e)}"
                st.error(response_text)

    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response_text})

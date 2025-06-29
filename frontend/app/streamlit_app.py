import streamlit as st
import requests
import os

# Read the backend URL from environment variable
backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Saviant RAG Assistant", layout="wide")
st.title("💬 Saviant RAG Chatbot")

query = st.text_input("🔍 Ask your question:")

if query:
    try:
        with st.spinner("Generating answer from backend..."):
            response = requests.post(
                f"{backend_url}/query",
                json={"question": query},
                timeout=30,
            )
            response.raise_for_status()
            answer = response.json().get("answer", "⚠️ No answer returned.")
        
        st.markdown("### 🧠 AI Answer")
        st.markdown(answer.strip().replace("\n", "  \n"))

    except Exception as e:
        st.error(f"❌ Error: {e}")

import sys
from pathlib import Path
import streamlit as st

# Setup project root path
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from logic.rag_pipeline import RAGPipeline

# ----------------------------
# Cached pipeline loader
# ----------------------------
@st.cache_resource
def load_pipeline():
    config_path = project_root / "config/app_config.yaml"
    return RAGPipeline(config_path=str(config_path))

pipeline = load_pipeline()

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Saviant RAG Assistant", layout="wide")
st.title("💬 Saviant RAG Chatbot")

query = st.text_input("🔍 Ask your question:")

if query:
    try:
        with st.spinner("Generating answer and retrieving documents..."):
            answer = pipeline.invoke(query)

        # 🧠 Render AI Answer with proper line breaks
        st.markdown("### 🧠 AI Answer")
        st.markdown(answer.strip().replace("\n", "  \n"))

        # 📄 Optional: Show retrieved documents as context
        if hasattr(pipeline.retriever, "_vectorstore") and hasattr(pipeline.retriever._vectorstore, "similarity_search_with_score"):
            docs_with_scores = pipeline.retriever._vectorstore.similarity_search_with_score(query, k=pipeline.k)

            st.markdown("### 📄 Source Context")
            for i, (doc, score) in enumerate(docs_with_scores, start=1):
                content = doc.page_content.strip().replace("\n", " ")
                st.markdown(f"**[{i}] Score: {score:.4f}**  \n{content[:500]}...")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# 🧠 Saviant RAG Assistant

A Retrieval-Augmented Generation (RAG) assistant built using LangChain, LangSmith, FastAPI, and Google Cloud.

## 🔍 Features
- RAG with document-specific context
- LangSmith-based evaluation on correctness, relevance, groundedness, and retrieval quality
- Modular FastAPI backend
- CI/CD-ready architecture with Jenkins
- Google Cloud deployable

## 🚀 Getting Started

```bash
git clone <repo-url>
cd saviant_app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt




rag-assistant/
│
├── backend/                      # FastAPI backend with socket handlers
│   ├── server.py
│   └── socket_events.py
│
├── config/                       # YAML configs for app, retrieval, indexing
│   ├── app_config.yaml
│   ├── indexing_config.yaml
│   └── retrieval_config.yaml
│
├── data/                         # Indexed vector DB and input documents
│   ├── docs/
│   └── vector_db/
│
├── frontend/                     # Streamlit & web UI clients
│   ├── streamlit/
│   │   └── streamlit_app.py
│   └── web_ui/
│
├── logic/                        # Core RAG logic and pipelines
│   ├── llm.py
│   ├── retriever.py
│   ├── rag_pipeline.py
│   ├── rag_chain.py
│   └── indexing_pipeline.py
│
├── prompts/                      # Prompt templates and evaluation prompts
│   ├── json_prompts/
│   │   ├── rag_template_v1.json
│   │   └── rag_template_v2.json
│   └── rag_evaluation/
│       └── metrices_prompts.py
│
├── tests/                        # Unit, integration, and evaluation tests
│   ├── unit/
│   ├── integration/
│   └── evaluation/
│       ├── rag_test_dataset.csv
│       ├── golden_queries.csv
│       └── run_rag_eval.py
│
├── main.py                       # App entry point
├── requirements.txt              # Python dependencies
├── README.md                     # Project overview
└── .gitignore

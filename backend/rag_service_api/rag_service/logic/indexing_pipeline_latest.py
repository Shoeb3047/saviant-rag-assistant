import os
import yaml
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


class IndexingPipeline:
    def __init__(self, config_path: str):
        self.project_root = Path(__file__).resolve().parents[1]  # Points to <project_root>/
        self.config = self._load_config(self.project_root / config_path)

        self.documents_dir = self.project_root / self.config["data_dir"]
        self.doc_version = self.config["doc_version"]
        self.chunk_size = self.config["chunk_size"]
        self.chunk_overlap = self.config["chunk_overlap"]
        self.embedding_model = self.config["embedding_model"]
        self.vector_db_cfg = self.config["vector_db"]
        self.document_sources = self._get_document_sources()

        self.all_documents = []
        self.docs_chunks = []

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        self.vectorstore = Chroma(
            collection_name=self.vector_db_cfg["collection_name"],
            embedding_function=self.embeddings,
            persist_directory=str(self.project_root / self.vector_db_cfg["persist_dir"])
        )

    def _load_config(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def _get_document_sources(self):
        return [
            str(file.resolve())
            for file in self.documents_dir.glob("*")
            if file.suffix in [".pdf", ".txt", ".csv"]
        ]

    def load_documents_files(self):
        for source in self.document_sources:
            try:
                loader = WebBaseLoader(source) if source.startswith("http") else PyPDFLoader(source)
                documents = loader.load()
                self.all_documents.extend(documents)
                print(f"✅ Loaded {len(documents)} documents from {source}")
            except Exception as e:
                print(f"❌ Error loading {source}: {e}")

        if not self.all_documents:
            raise RuntimeError("No documents were loaded. Aborting.")

    def split_documents(self):
        self.docs_chunks = self.text_splitter.split_documents(self.all_documents)
        print(f"📚 Split into {len(self.docs_chunks)} chunks")

    def create_add_vector_db(self):
        if self.vectorstore._collection.count() > 0:
            print("⚠️ Vectorstore already exists. Skipping creation.")
            return

        self.load_documents_files()
        self.split_documents()
        ids = [f"{self.doc_version}_chunk_{i}" for i in range(len(self.docs_chunks))]
        self.vectorstore.add_documents(documents=self.docs_chunks, ids=ids)
        print("✅ Vectorstore created and persisted.")


if __name__ == "__main__":
    pipeline = IndexingPipeline(config_path="config/indexing_config.yaml")
    pipeline.create_add_vector_db()

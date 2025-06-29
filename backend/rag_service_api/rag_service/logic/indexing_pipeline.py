import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def get_file_type(file_name:str)->str:
    """_summary_

    Args:
        file_name (str): File Name in string 

    Returns:
        file_type : Return File type for Document loader (str)
    """
    if file_name.startswith("http") or file_name.startswith("https"):
        file_type = "web_pages"
    elif file_name.endswith(".pdf"):
        file_type = "pdf"
    elif file_name.endswith(".txt"):
        file_type ="txt"
    elif file_name.endswith(".csv"):          
        file_type = "csv"
    else:
        raise(f"Document file type for file {file_name} is not supported.")
    


def dynamic_document_loader(file_type):
    if file_type =="pdf":
        # return PDF Loader 
        pass
    elif file_type =="txt":
        # return document
        pass 
    elif file_type =="web_pages":
        # return Web Page Loader 
        pass
    else:
        raise(f"File type {file_type} is not supported")



class RagVectorDB:
    def __init__(self, document_sources,collection_name="rag_bot_vector_db_v1"):
        self.document_sources = document_sources
        self.all_documents = []
        self.docs_chunks = []
        self.k = 4  # Top-K results to retrieve

        # Text Splitter initialization
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        # Embedding initialization
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Vector store config
        self.persistent_directory = "/Users/shoeb/Desktop/VS_Code/LLMOpps/rag_bot/rag_vector_databases"
        self.collection_name = collection_name

        # Load or create vectorstore
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persistent_directory
        )

    def load_documents_files(self):
        for source in self.document_sources:
            try:
                loader = WebBaseLoader(source) if source.startswith("http") else PyPDFLoader(source)
                documents = loader.load()
                self.all_documents.extend(documents)
                print(f"Loaded {len(documents)} documents from {source}")
            except Exception as e:
                print(f"Error loading {source}: {e}")
        
        if self.all_documents == []:
            raise("Not able to load documents , aborting !!!!")
        print(f"Total documents loaded: {len(self.all_documents)}")


    def split_documents(self):
        self.docs_chunks = self.text_splitter.split_documents(self.all_documents)
        print(f"Split into {len(self.docs_chunks)} chunks")

    def create_add_vector_db(self):
        if self.vectorstore._collection.count() > 0:
            print("Vectorstore already exists. Skipping creation.")
            return

        self.load_documents_files()
        self.split_documents()
        ids = [f"chunk_{i}" for i in range(len(self.docs_chunks))]
        self.vectorstore.add_documents(documents=self.docs_chunks,ids=ids)
        print("Vectorstore created and persisted.")

    def query_with_score(self, query_text):
        return self.vectorstore.similarity_search_with_score(query_text, k=self.k)
    
    
    
    
def main(document_sources):
    rag_vector_db_obj = RagVectorDB(document_sources)
    rag_vector_db_obj.create_add_vector_db()
    

if __name__ =='__main__':
    source_dir = "/Users/shoeb/Desktop/VS_Code/LLMOpps/rag_bot/public/data"
    documents_files = ['LangGraph Tutorial for Beginners.pdf', 'llmOperations.pdf', 'A Comprehensive Guide to Building Agentic RAG Systems with LangGraph.pdf']
    document_sources =  [ os.path.join(source_dir,file_name) for file_name in documents_files ]
    print(document_sources)
    print(os.listdir())
    # main(document_sources)
        
        

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def get_retriever(
    persist_dir: str,
    collection_name: str = "default",
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    k: int = 3
):
    """
    Load a retriever from an existing Chroma vector DB collection.

    Args:
        persist_dir (str): Directory where Chroma DB is stored.
        collection_name (str): Name of the Chroma collection to load.
        model_name (str): Name of the embedding model.
        k (int): Number of similar documents to retrieve.

    Returns:
        A retriever object that can be used for querying.
    """
    embedding_model = HuggingFaceEmbeddings(model_name=model_name)

    vectorstore = Chroma(
        collection_name=collection_name,
        persist_directory=persist_dir,
        embedding_function=embedding_model
    )

    return vectorstore.as_retriever(search_kwargs={"k": k})

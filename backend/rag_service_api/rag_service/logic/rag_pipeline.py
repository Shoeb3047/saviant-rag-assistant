import sys
from pathlib import Path

# Add project root to PYTHONPATH
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))



import yaml
import logging
from pathlib import Path
from langchain_core.prompts import load_prompt
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from logic.retriever import get_retriever  # ✅ FIXED: use shared retriever logic
from dotenv import load_dotenv
load_dotenv()

# x = load_dotenv()
# print(x)

class RAGPipeline:
    def __init__(self, config_path: str):
        self.project_root = Path(__file__).resolve().parents[1]  # <== logic/ -> project root
        self.config_path = self._resolve_path(config_path)
        self.config = self._load_config()

        # Configure logging
        logging_level = self.config.get("logging_level", "INFO").upper()
        logging.basicConfig(level=getattr(logging, logging_level))
        self.logger = logging.getLogger(__name__)

        # Extract configs
        self.k = self.config.get("k", 5)
        self.llm_config = self.config["llm"]
        self.prompt_config = self.config["prompt"]
        self.vector_db_config = self.config["vector_db"]

        # Components
        self.retriever = self._load_retriever()
        self.prompt = self._load_prompt()
        self.llm = self._load_llm()
        self.chain = self._build_chain()

    def _resolve_path(self, path_str: str) -> Path:
        path = Path(path_str)
        return path if path.is_absolute() else self.project_root / path

    def _load_config(self):
        with open(self.config_path, "r") as f:
            return yaml.safe_load(f)

    def _load_prompt(self):
        prompt_path = self._resolve_path(self.prompt_config["template"])
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt template not found at: {prompt_path}")
        return load_prompt(str(prompt_path))

    def _load_llm(self):
        provider = self.llm_config.get("provider")
        temperature = self.llm_config.get("temperature", 0.7)
        max_tokens = self.llm_config.get("max_tokens", 512)

        if provider == "groq":
            return ChatGroq(
                model=self.llm_config["model"],
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            raise ValueError(f"LLM provider '{provider}' is not supported yet.")

    def _load_retriever(self):
        return get_retriever(
            persist_dir=str(self._resolve_path(self.vector_db_config["persist_dir"])),
            collection_name=self.vector_db_config["collection_name"],
            model_name=self.vector_db_config.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2"),
            k=self.k
        )

    def _build_chain(self):
        self.retriever_chain = RunnableParallel({
            "context": self.retriever,
            "question": RunnablePassthrough()
        })
        self.generation_chain = self.prompt | self.llm | StrOutputParser()
        return self.retriever_chain | self.generation_chain
        #return self.retriever_chain | self.prompt | self.llm | StrOutputParser()

    def get_retreiver_chain(self):
        return self.retriever_chain
    
    def get_generation_chain(self):
        return self.generation_chain
    
    def invoke(self, query: str):
        self.logger.info(f"🔍 Invoking RAG pipeline for query: {query}")
        return self.chain.invoke(query)



# Pipeline test 
# if __name__ == "__main__":
#     pipeline = RAGPipeline(config_path="config/app_config.yaml")
#     question = "Tell me about the setting Require Request Review Comments?"
#     result = pipeline.retriever_chain.invoke(question)
#     docs = result['context']
#     question = result['question']
    
#     for i,doc in enumerate(docs):
#         print(f"doc {i} : {doc}")
#     print(f"question : {question}")
    
#     ai_answer = pipeline.generation_chain.invoke(result)
#     print(f"AI answer {ai_answer}")
    
    


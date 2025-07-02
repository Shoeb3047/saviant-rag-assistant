from langchain_core.prompts import load_prompt
from logic.retriever import get_retriever
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import logging
import yaml


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#############
def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_prompt_from_json(prompt_path: str):
    prompt = load_prompt(prompt_path)
    return prompt 


def build_chain(config):
    # Load config values
    rag_config = config["rag"]
    llm_config = config["llm"]

    # Retriever
    retriever = get_retriever(
        persist_dir=rag_config["persist_dir"],
        collection_name=rag_config["collection_name"],
        k=rag_config["k"]
    )

    # Prompt
    prompt = get_prompt_from_json(rag_config["prompt_path"])

    # LLM
    llm = ChatGroq(model=llm_config["model_name"])

    # Parallel chain
    parallel_chain = RunnableParallel(
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
    )
    # Final chain
    return parallel_chain | prompt | llm | StrOutputParser()


# if __name__ =="__main__":
#     # these values should come from yaml files in future 
#     # prompt_path = "/Users/shoeb/Desktop/VS_Code/LLMOpps/rag_bot/prompts/rag_qa_template.json"
#     # persist_dir="/Users/shoeb/Desktop/VS_Code/LLMOpps/rag_bot/rag_vector_databases"
#     # collection_name="rag_bot_vector_db_v1"
#     # k=5
    
#     config = load_config("config/retreival.yaml")
#     chain = build_chain(config)
    
    
#     # test main chain 
#     result = chain.invoke("What is Agentic AI? Summarize in 5 points.")
    
#     print(result)
    




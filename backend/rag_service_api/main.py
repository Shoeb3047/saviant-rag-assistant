from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_service.logic.rag_pipeline import RAGPipeline
import os

class QueryInput(BaseModel):
    question: str

app = FastAPI()

@app.get("/")
def read_root():
    groq_key = os.getenv("GROQ_API_KEY", "NOT SET")
    print(f"GROQ_API_KEY from env: {groq_key[:5]}...")  # Logs

    return {
        "message": "Saviant RAG service is up and running! NEW BUILD!!!",
        "groq_key_prefix": groq_key[:5] + "..." if groq_key != "NOT SET" else "NOT SET"
    }


pipeline = RAGPipeline(config_path="config/app_config.yaml")

@app.post("/query")
def get_answer(query: QueryInput):
    try:
        answer = pipeline.invoke(query.question)
        return {"answer": answer}
        # groq_key = os.getenv("GROQ_API_KEY", "NOT SET")
        # print(f"GROQ_API_KEY from env: {groq_key[:5]}...")  # Avoid printing full key in logs

        # return {"answer": f"Dummy response for (GROQ_API_KEY from env: {groq_key[:5]}...) : {query.question}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




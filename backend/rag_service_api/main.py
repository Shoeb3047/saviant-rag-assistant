from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_service.logic.rag_pipeline import RAGPipeline

class QueryInput(BaseModel):
    question: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Saviant RAG service is up and running!"}

pipeline = RAGPipeline(config_path="config/app_config.yaml")

@app.post("/query")
def get_answer(query: QueryInput):
    try:
        answer = pipeline.invoke(query.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

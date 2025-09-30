from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from rag.rag_pipeline import QueryPipeline

load_dotenv()
app = FastAPI()

# Allow React frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline once (loads embeddings/vector store)
query_pipeline = QueryPipeline()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_question(req: QueryRequest):
    """Accepts a query and returns an LLM answer."""
    answer = query_pipeline.ask(req.query)
    return {"query": req.query, "answer": answer}

# ✅ Only runs when you do: python main.py to run it manually
if __name__ == "__main__":
    q = "Why are tailored hydromet services and robust early warning systems critical for Bangladesh?"
    print("Q:", q)
    print("A:", query_pipeline.ask(q))
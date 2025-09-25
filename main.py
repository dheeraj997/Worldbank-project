import os
from dotenv import load_dotenv
from rag.rag_pipeline import QueryPipeline

load_dotenv()

if __name__ == "__main__":

    # --- Run query frequently ---
    query_pipeline = QueryPipeline()
    q = "Why are tailored hydromet services and robust early warning systems critical for Bangladesh?"
    print("Q:", q)
    print("A:", query_pipeline.ask(q))

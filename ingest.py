import os
from dotenv import load_dotenv
from rag.rag_pipeline import IngestionPipeline

load_dotenv()

if __name__ == "__main__":
    bucket = os.getenv("BUCKET_NAME")
    prefix = os.getenv("S3_PREFIX")

    ingestion = IngestionPipeline(bucket, prefix)
    ingestion.run()

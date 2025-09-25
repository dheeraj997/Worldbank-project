import boto3
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from typing import List



def process_all_pdfs_from_s3(bucket_name: str, prefix: str = "") -> List:

    s3 = boto3.client("s3")
    """
    Load all PDFs from an S3 bucket (downloads to temporary files in memory).

    Args:
        bucket_name: Name of the S3 bucket
        prefix: Optional S3 prefix/folder

    Returns:
        List of LangChain document objects
    """
    all_documents = []

    # List objects in the S3 bucket
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if "Contents" not in response:
        print(f"No files found in s3://{bucket_name}/{prefix}")
        return []

    # Filter PDF files
    pdf_files = [obj["Key"] for obj in response["Contents"] if obj["Key"].endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDFs in s3://{bucket_name}/{prefix}")

    for pdf_key in pdf_files:
        try:
            # Download PDF from S3
            pdf_obj = s3.get_object(Bucket=bucket_name, Key=pdf_key)
            pdf_bytes = pdf_obj["Body"].read()

            # Write to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(pdf_bytes)
                tmp.flush()

                # Load PDF using PyPDFLoader
                loader = PyPDFLoader(tmp.name)
                documents = loader.load()

                # Add metadata
                for doc in documents:
                    doc.metadata["source_file"] = pdf_key
                    doc.metadata["file_type"] = "pdf"

                all_documents.extend(documents)

            print(f"Loaded {len(documents)} pages from {pdf_key}")

        except Exception as e:
            print(f"Error loading {pdf_key}: {e}")

    print(f"Total documents loaded: {len(all_documents)}")
    return all_documents

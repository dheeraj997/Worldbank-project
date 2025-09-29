# RAG Retriever Project

A **RAG (Retrieval-Augmented Generation) system** that loads PDFs from AWS S3, creates embeddings, stores them in ChromaDB, and answers user queries using an LLM. FastAPI is used as a backend API, and React can be used for the frontend interface.

A **RAG (Retrieval-Augmented Generation) system** that allows semantic querying of PDFs.

- **Backend:** Python + FastAPI
- **Frontend:** React (optional)
- **Vector Database:** ChromaDB
- **Embeddings:** SentenceTransformers
- **LLM:** Groq API

---

## 🖼 Architecture Diagram

![RAG Pipeline Diagram](diagram.png)

**Flow:**

1. **AWS S3** → Store PDFs
2. **PDF Loader** → Download PDFs and extract text
3. **Splitter** → Break text into smaller chunks
4. **Embeddings** → Convert chunks into vectors
5. **Vector Store (ChromaDB)** → Store embeddings for semantic search
6. **Retriever** → Query top relevant chunks
7. **LLM (Groq)** → Generate answers using context
8. **FastAPI** → Expose backend API
9. **React Frontend** → Input query + display answer (optional)

---

## 🟢 Setup

### 1. Virtual Environment

Create and manage a Python virtual environment:

```bash
# Install uv (virtual environment manager)
pip install uv

# Initialize virtual environment
uv init

# Activate virtual environment
.venv\Scripts\activate

# Install project dependencies
uv add -r .\requirements.txt

--------------------------------------------------------------------------------------------------
git commands

--git init

--git remote set-url origin "repository name"

--git add .

--git commit -m"message"

--git push origin main
--------------------------------------------------------------------------------------------------
aws commands

# Configure AWS with IAM credentials
aws configure

# List all S3 buckets
aws s3 ls

---------------------------------------------------------------------------------------------------
fast api server commands

# to run the sever
--uvicorn main:app --reload
---------------------------------------------------------------------------------------------------
react commands

# Clear npx cache if needed
npx clear-npx-cache

# Create a new React app
npx create-react-app@latest frontend

# Start React development server
npm start

----------------------------------------------------------------------------------------------------
final product

image.png
```

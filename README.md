# Academic Question Answering System Using RAG

An AI-powered academic question-answering system built using **Retrieval-Augmented Generation (RAG)**. The system retrieves relevant information from academic documents using semantic search and provides document-grounded answers through a Gemini LLM.

The current V1 knowledge base uses **Operating Systems study material**.

## 📌 Project Overview

Students often need to search through large amounts of academic material to find definitions, concepts, algorithms, and syllabus topics.

This project provides a conversational interface where students can ask questions in natural language and receive answers based on the indexed academic documents.

Instead of relying only on an LLM's general knowledge, the system:
1. Converts academic document chunks into embeddings.
2. Stores the embeddings in Pinecone.
3. Converts the user's question into an embedding.
4. Retrieves the most relevant document chunks.
5. Sends the retrieved context to Gemini.
6. Generates a grounded academic answer.

## 🧠 RAG Workflow

```text
                    OFFLINE / INGESTION
Academic PDF
     ↓
PyPDFLoader
     ↓
Text Chunking
     ↓
Jina Embeddings
     ↓
Pinecone Vector Database


                    ONLINE / QUESTION ANSWERING
Student Question
     ↓
Jina Query Embedding
     ↓
Pinecone Similarity Search
     ↓
Relevant Document Chunks
     ↓
Grounded Prompt
     ↓
Gemini LLM
     ↓
Academic Answer
     ↓
Retrieved Sources / Page References
```

## ✨ Current Features

- 📄 PDF-based academic document ingestion
- ✂️ Recursive text chunking
- 🧠 Jina hosted embeddings
- 🗄️ Pinecone vector database
- 🔎 Semantic similarity search
- ⚡ Adaptive Top-K retrieval
  - Top 5 for normal questions
  - Top 10 for conceptual questions
  - Top 50 for broad/complete-syllabus questions
- 🤖 Gemini-based answer generation
- 📚 Context-grounded academic responses
- 🛡️ Protection against inventing missing syllabus content
- 🔁 Retry handling for temporary Gemini API failures
- 💬 Streamlit conversational interface
- 📖 Retrieved source chunks and page numbers displayed with answers

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| UI | Streamlit |
| Document Loading | LangChain PyPDFLoader |
| Text Splitting | LangChain RecursiveCharacterTextSplitter |
| Embeddings | Jina `jina-embeddings-v5-text-small` |
| Vector Database | Pinecone |
| LLM | Google Gemini |
| API Client | `google-genai` |
| Environment Variables | `python-dotenv` |
| HTTP Requests | `requests` |

## 📁 Project Structure

```text
## 📁 Project Structure

```text
HCL_RAG_Project/
│
├── Academic-RAG/
│   ├── .env
│   ├── app.py
│   ├── os_notes.pdf
│   └── rag_V1.ipynb
│
├── Documentation/
│   ├── Academic_RAG_Project_Documentation.pdf
│   └── Academic_RAG_SRS_V1.pdf
│
├── .gitignore
├── README.md
└── requirements.txt
```

| File | Purpose |
|---|---|
| `os_notes.pdf` | Operating Systems academic knowledge base |
| `rag.ipynb` | Development notebook containing the V1 RAG pipeline |
| `app.py` | Streamlit application providing the interactive RAG interface |
| `requirements.txt` | Python dependencies required by the project |
| `README.md` | Project documentation |
| `.env` | API keys and secrets; should never be committed |

## ⚙️ How the System Works

### 1. Document Processing
The academic PDF is loaded using LangChain's `PyPDFLoader` and divided into smaller chunks using `RecursiveCharacterTextSplitter`.

### 2. Embedding Generation
Each chunk is converted into a numerical vector using Jina's hosted model:

```text
jina-embeddings-v5-text-small
```

The vectors are normalized and stored in Pinecone.

### 3. Query Processing
When a student asks a question, the question is converted into the same embedding space. Pinecone performs cosine-similarity search to retrieve relevant chunks.

### 4. Adaptive Retrieval

```text
Normal question       → Top 5
Conceptual question   → Top 10
Broad/complete query  → Top 50
```

### 5. Grounded Generation
Retrieved chunks are placed into a prompt and sent to Gemini. The prompt instructs the model to use only the supplied context and avoid inventing missing syllabus information.

### 6. Source Display
The Streamlit application displays retrieved document chunks and page numbers under **View Retrieved Sources**.

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
JINA_API_KEY=your_jina_api_key
PINECONE_API_KEY=your_pinecone_api_key
GEMINI_API_KEY=your_gemini_api_key
```

**Never upload `.env` to GitHub.**

Recommended `.gitignore` entry:

```text
**/.env
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Academic-RAG
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create `.env` and add the Jina, Pinecone, and Gemini API keys.

## ▶️ Run the Streamlit Application

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## 📓 Run the Development Notebook

The development and experimentation pipeline is available in:

```text
rag.ipynb
```

It covers:

```text
PDF Loading
    ↓
Text Chunking
    ↓
Jina Embeddings
    ↓
Pinecone Indexing
    ↓
Query Embedding
    ↓
Retrieval
    ↓
Adaptive Top-K
    ↓
Gemini Generation
    ↓
End-to-End Testing
```

## 🧪 Example Questions

```text
What is a process in an operating system?

Explain deadlock prevention.

What is virtual memory?

Explain the difference between paging and segmentation.

What are the page replacement algorithms?

Give an overview of the Operating Systems syllabus.
```

## 📊 Current V1 Status

**Status: V1 Prototype / Development**

### Implemented

- PDF ingestion
- Text chunking
- Cloud embeddings
- Pinecone vector storage
- Semantic retrieval
- Adaptive Top-K retrieval
- Grounded Gemini generation
- Source/page display
- Streamlit chat interface

### Not yet implemented

- Multi-subject knowledge base
- Subject-aware metadata filtering
- Hybrid keyword + vector retrieval
- Retrieval reranking
- Automated retrieval evaluation
- User authentication
- Persistent chat history
- Production cloud deployment

## 🔮 Future Upgrades

### V1.1 — Multi-Subject Support
Expand the knowledge base to subjects such as Operating Systems, DBMS, DAA, Computer Networks, and Web Technology, with subject metadata and subject-specific retrieval.

### V1.2 — Retrieval Quality
Improve chunking, add similarity thresholds, evaluate Recall@K and MRR, improve source citation, and reduce irrelevant chunks.

### V1.3 — Advanced Retrieval
Add hybrid search, reranking, better query processing, and query expansion.

### V2 — Academic Platform
Add multi-subject UI, student accounts, persistent conversation history, cloud deployment, administrative document upload, and a larger academic knowledge base.

### Long-Term Vision
The system can evolve from a single-subject academic assistant into a scalable academic knowledge platform by progressively expanding the document corpus, retrieval quality, subject metadata, and cloud infrastructure.

## 📌 Security Note

API keys must be stored in environment variables and must not be hard-coded into source files.

Do not commit `.env` to GitHub.

## 👨‍💻 Author

**Bhaskar Pandey**

Computer Science Engineering

Academic RAG Project
